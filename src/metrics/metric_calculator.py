import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from metrics.types.agent_dataframe import PCADataSchema

from .types import AgentSchema


class MetricCalculator:
    """Class to calculate metrics used in the simulation."""

    @staticmethod
    def calculate_true_fst(df: DataFrame[AgentSchema]) -> float:
        """
        Calculate FST for a given DataFrame.

        Args:
            df: DataFrame containing 'population_type' and 'agent_dna' columns.

        Returns:
            Average FST across all loci.

        """
        dna_list_a = df[df["population_type"] == "A"]["agent_dna"].tolist()
        dna_list_b = df[df["population_type"] == "B"]["agent_dna"].tolist()

        # Convert binary strings to a 2D numpy array (rows: agents, cols: loci)
        arr_a = np.array([list(map(int, dna)) for dna in dna_list_a])
        arr_b = np.array([list(map(int, dna)) for dna in dna_list_b])

        if arr_a.size == 0 or arr_b.size == 0:
            return 0.0

        # Calculate allele frequencies (p) for each locus
        p_a = np.mean(arr_a, axis=0)
        p_b = np.mean(arr_b, axis=0)
        p_total = np.mean(np.concatenate([arr_a, arr_b]), axis=0)

        # Heterozygosity (H = 2p(1-p))
        h_s = (2 * p_a * (1 - p_a) + 2 * p_b * (1 - p_b)) / 2
        h_t = 2 * p_total * (1 - p_total)

        # FST = (Ht - Hs) / Ht
        # Avoid division by zero for fixed loci
        fst_per_locus = np.divide(
            h_t - h_s, h_t, out=np.zeros_like(h_t), where=h_t != 0
        )

        return np.mean(fst_per_locus)

    @staticmethod
    def calculate_bhattacharyya_distance(
        df: DataFrame[AgentSchema], trait: str
    ) -> float:
        """
        Calculate B-distance for a specific trait.

        Args:
            df: DataFrame containing 'population_type' and the specified trait columns.
            trait: The name of the trait column to analyze.

        Returns:
            The B-distance between the two populations for the specified trait.

        """
        a_data: pd.Series[int] = df[df["population_type"] == "A"][trait]
        b_data: pd.Series[int] = df[df["population_type"] == "B"][trait]

        if len(a_data) < 2 or len(b_data) < 2:
            return 0.0

        mu1, mu2 = a_data.mean(), b_data.mean()
        var1 = a_data.var()
        var2 = b_data.var()

        if var1 == 0 or var2 == 0:
            return 0.0

        # Gaussian B-distance
        # fmt: off
        term1 = 0.25 * np.log(0.25 * ((var1 / var2) + (var2 / var1) + 2))  # pyrefly: ignore
        term2 = 0.25 * ((mu1 - mu2) ** 2 / (var1 + var2))  # pyrefly: ignore
        # fmt: on
        return term1 + term2

    @staticmethod
    def calculate_pca(
        df: DataFrame[AgentSchema], n_components: int = 2
    ) -> DataFrame[PCADataSchema]:
        """
        Calculate PCA for a given DataFrame.

        Args:
            df: DataFrame containing the features to analyze.
            n_components: Number of principal components to compute.

        Returns:
            PCA result as a numpy array with shape (n_samples, n_components).

        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_cols])

        pca = PCA(n_components=n_components)
        components = pca.fit_transform(scaled_data)

        result_df = pd.DataFrame(
            components, columns=[f"pc{i + 1}" for i in range(n_components)]
        )
        result_df["population_type"] = df["population_type"].values

        return DataFrame[PCADataSchema](result_df)
