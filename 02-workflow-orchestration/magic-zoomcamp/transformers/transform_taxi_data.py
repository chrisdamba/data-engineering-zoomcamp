import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def camel_to_snake(name):
    import re
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    print("Total rows with 0 passengers:", data['passenger_count'].isin([0]).sum())
    print("Total rows with 0 trips:", data['trip_distance'].isin([0]).sum())
    print("vendor ids ", list(data['VendorID'].unique()))

    df = data[~((data['passenger_count'] == 0) & (data['trip_distance'] == 0))]
    df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
    df.columns = [camel_to_snake(column) for column in df.columns]

    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    print("Total rows vendor_ids with 1, 2:", output['vendor_id'].isin([1, 2]).sum()) 
    print("vendor ids ", list(output['vendor_id'].unique()))
    # Assert that there are no rows with passenger count equal to 0 AND trip distance equal to 0
    assert ((output['passenger_count'] == 0) & (output['trip_distance'] == 0)).sum() == 0, 'There are no rides with zero passengers and no distance'

    # 1. Assertion for `vendor_id` being one of the existing, acceptable values
    assert output['vendor_id'].isin([1, 2, pd.NA]).all(), "There are invalid vendor_id values"

    # 2. Assertion for `passenger_count` being greater than 0
    # assert (output['passenger_count'] == 0).sum() == 0, "There are no rides with zero passengers"

    # 3. Assertion for `trip_distance` being greater than 0
    # assert (output['trip_distance'] == 0).sum() == 0, "There are no rides with 0 trip_distance"
