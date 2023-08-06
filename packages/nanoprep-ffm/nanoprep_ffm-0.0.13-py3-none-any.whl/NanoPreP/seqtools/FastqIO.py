from NanoPreP.seqtools.SeqFastq import SeqFastq
from io import TextIOWrapper
from pathlib import Path
import gzip

class FastqIO:
    # FASTQ generator
    def read(handle: TextIOWrapper) -> SeqFastq:
        # reading from the handle
        for line in handle:
            yield SeqFastq.parse(
                line,
                next(handle),
                next(handle),
                next(handle)
            )

    # write SeqFastq to files in FASTQ format
    def write(handle: TextIOWrapper, record: SeqFastq) -> None:
        handle.write(str(record))
        return

class FastqIndexIO:
    def __init__(self, file: str) -> None:
        self.file = file
        self.names, self.offsets = FastqIndexIO.fqidx(file)
        return
        
    @staticmethod
    def openg(p:str, mode:str):
        p = Path(p) if not isinstance(p, Path) else p
        if p.suffix == ".gz":
            return gzip.open(p, mode + "t")
        else:
            return open(p, mode)
        
    # index FASTQ file
    @staticmethod
    def fqidx(file: str) -> dict:
        # index the handle
        ordered_keys = []
        offsets = {}
        with FastqIndexIO.openg(file, "r") as handle:
            while True:
                offset = handle.tell()
                identifier = handle.readline().strip()
                if len(identifier) == 0:
                    break
                ordered_keys.append(identifier[1:])
                offsets[identifier[1:]] = offset
                handle.readline()
                handle.readline()
                handle.readline()
        return ordered_keys, offsets
    

    # get SeqFastq using index
    def get(self, name: str) -> SeqFastq:
        with FastqIndexIO.openg(self.file, "r") as handle:
            handle.seek(self.offsets[name])
            return SeqFastq.parse(
                handle.readline(),
                handle.readline(),
                handle.readline(),
                handle.readline()
            )
    
    # iter
    def __iter__(self):
        for name in self.names:
            yield self.get(name)
        return