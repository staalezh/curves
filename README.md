This tool was written as part of my [thesis] (https://www.duo.uio.no/handle/10852/45384?locale-attribute=en)
«On the Generation of Strong Elliptic Curves for Cryptographic Applications»,
and was used to generate elliptic curves and Edwards curves that are resistent
to known attacks on the ECDLP.


## Usage
```bash
$ sage main.py [--num-proc NUM\_PROC] [--point-compression]
               [--overrun-protection]
               (--base-field BASE_FIELD | --num-bits NUM_BITS)
               outfile
```

* The point compression flag requries that the chose base field (if not
specified) should satisfy p = 3 (mod 4). This allows for efficient point
compression.

* The overrun protection flag is used to indicate that we want an elliptic curve
E such that #E(\F_q) < q. This may be convenient for curve implementers as
the bit length of #E(\F_q) in may exceed the bit lenght of q.

