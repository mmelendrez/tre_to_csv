# nwk_to_csv

## Install

1. Install compiler to compile biopython

   ```
   sudo yum install gcc gcc-c++
   ```

1. Install latest development for biopython (v1.69)

   ```
   pip install git+https://github.com/biopython/biopython.git
   ```


## Usage

### Traditional way

```
python tre_to_csv.py <input.tre>
```

### Another way using docker

This removes the need to worry about dependencies and will always run the same
way regardless of computer

1. Only once do you have to build the docker image

   ```
   docker build -t local/biopython .
   ```

1. Then you can execute the code using docker

   ```
   docker run -it -v $PWD:/here -w /here local/biopython python tre_to_csv.py examples/test.tre
   ```

## Output

output will go to standard output 

## Examples

```
python tre_to_csv.py examples/test.tre
```

## Taxnames

Make sure not to have dashes in your taxnames or it will break at this time due
to https://github.com/biopython/biopython/issues/1022
