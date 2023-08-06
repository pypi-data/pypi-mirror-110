# OceanIA query

A small package to query data from the OceanIA services

## Install

Install using `pip`

```bash
> pip install oceania-query-fasta
```

## Usage

The library may be used directly as a command line tool or imported as a python package

### Command line

In the command line:

```bash
> oceania query-fasta <key> <query_file> <output_format> <output_file>
```

For more information information:

```bash
> oceania query-fasta -h
Usage: oceania query-fasta [OPTIONS] <key> <query_file> <output_format> <output_file>

  Extract secuences from a fasta file in the OceanIA Storage.

  <key> object key in the OceanIA storage
  <query_file> CSV file containing the values to query.
               Each line represents a sequence to extract in the format "sequence_id,start,end,type"
               "sequence_id" sequence ID
               "start" start index position of the sequence to be extracted
               "end" end index position of the sequence to extract
               "type" type of the sequence to extract
                      options are ["raw", "complement", "reverse_complement"]
                      type value is optional, if not provided default is "raw"
  <output_format> results format
                  options are ["csv", "fasta"]
  <output_file> name of the file to write the results
```

#### Example

```bash
> oceania query-fasta data/raw/tara/OM-RGC_v2/assemblies/TARA_A100000171.scaftig.gz query.csv csv example.output.csv
```

query.csv:
```csv
TARA_A100000171_G_scaffold48_1,10,50,complement
TARA_A100000171_G_scaffold48_1,10,50,raw
TARA_A100000171_G_scaffold48_1,10,50,reverse_complement
TARA_A100000171_G_scaffold181_1,0,50
TARA_A100000171_G_scaffold181_1,100,200
TARA_A100000171_G_scaffold181_1,200,230
```

### As a python package

```python
from oceania import OceaniaClient

# Create a client instance
oceania_client = OceaniaClient()

# Execute a query
oceania_client.get_sequences_from_fasta_to_file(key, positions, output_format, output_file)
```

#### Example
```python
from oceania import OceaniaClient

oceania_client = OceaniaClient()

key = "data/raw/tara/OM-RGC_v2/assemblies/TARA_A100000171.scaftig.gz"
positions = [
    ["TARA_A100000171_G_scaffold48_1", 10, 50, "complement"],
    ["TARA_A100000171_G_scaffold48_1", 10, 50],
    ["TARA_A100000171_G_scaffold48_1", 10, 50, "reverse_complement"],
    ["TARA_A100000171_G_scaffold181_1", 0, 50],
    ["TARA_A100000171_G_scaffold181_1", 100, 200],
    ["TARA_A100000171_G_scaffold181_1", 200, 230],
]

oceania_client.get_sequences_from_fasta_to_file(
    key,
    positions,
    "csv",
    "test_output.csv"
)
```
