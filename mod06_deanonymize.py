import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    quasi_identifiers = ['age', 'gender', 'zip3']
    merged = pd.merge(anon_df, aux_df, on=quasi_identifiers, how='inner') #merge datasets on quasi-identifiers
    match_counts_anon = merged.groupby('anon_id')['anon_id'].transform('count') #
    match_counts_aux = merged.groupby('name')['name'].transform('count')
    unique_matches = merged[(match_counts_anon == 1) & (match_counts_aux)].copy()
    return unique_matches[['anon_id', 'name']].rename(columns={'name': 'matched_name'})

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    total_anon_records = len(anon_df)
    if total_anon_records > 0:
        return len(matches_df) / total_anon_records 
    
    else: 
        return 0.0

