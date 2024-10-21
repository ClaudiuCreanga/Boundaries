import pandas as pd
from pandas.testing import assert_frame_equal
import pytest


df = pd.read_csv("/Users/ccreanga/projects/Boundaries/TableS3_hamming_revised", sep="\t")
df1 = pd.read_csv("/Users/ccreanga/projects/Boundaries/TableS3_hamming", sep="\t")

assert_frame_equal(df, df1)