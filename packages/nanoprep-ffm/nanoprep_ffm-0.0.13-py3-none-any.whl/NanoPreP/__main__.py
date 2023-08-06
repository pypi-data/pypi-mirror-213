from NanoPreP.preptools.Annotator import Annotator
from NanoPreP.preptools.Processor import Processor
from NanoPreP.seqtools.FastqIO import FastqIO, FastqIndexIO
from NanoPreP.seqtools.SeqFastq import SeqFastq
from NanoPreP.paramtools.paramsets import Params, Defaults
from NanoPreP.paramtools.argParser import parser
from NanoPreP.optimize.__main__ import get_pid_counts, get_pid_cutoff
from datetime import datetime
from pathlib import Path
import sys
import json
import gzip

def get_params():
    # parse arguments
    args = parser.parse_args()

    # load default parameters as `params`
    params = Defaults.copy()

    # update `params` with parameter presets
    if args.mode:
        if args.mode in Params.keys():
            params.update(Params[args.mode])
        else:
            msg = "Available options to `--mode`: "
            opts = ", ".join([i.__repr__() for i in Params.keys()])
            raise Exception(msg + opts)

    # update `params` from config
    if args.config:
        config = json.load(open(args.config))
        params.update(config)

    # update `params` with command line arguments (if specified)
    for k, v in vars(args).items():
        # skip flag arguments if their value are False
        if v == False:
            continue
        # skip un-specifed arguments
        if v != None:
            params[k] = v
            
    # optimize pid_cutoff if not `--disable_annot` and `--precision`
    if not params["disable_annot"]:
        # optimize pid_cutoff if `--precision` is specified   
        if params["precision"]:                
            # get pid counts
            SAMPLED, counters = get_pid_counts(
                p5_sense=params["p5_sense"],
                p3_sense=params["p3_sense"],
                isl5=params["isl5"],
                isl3=params["isl3"],
                input_fq=params["input_fq"],
                n=params["n"],
                skip_short=params["skip_short"],
                skip_lowq=params["skip_lowq"]
            )
            params["pid_isl"] = params["pid_body"]= get_pid_cutoff(
                counters,
                params["precision"]
            )
    return params


# open output files
def openg(p:Path, mode:str):
    if p.suffix == ".gz":
        return gzip.open(p, mode + "t")
    else:
        return open(p, mode)


def run(params:dict, rnames:list, batch_id: int, report_dict:dict, indexed_fq: FastqIndexIO):
    ## initiate Annotator
    annotator = Annotator(
        p5_sense=params["p5_sense"],
        p3_sense=params["p3_sense"],
        isl5=params["isl5"],
        isl3=params["isl3"],
        pid_isl=params["pid_isl"],
        pid_body=params["pid_body"],
        w=params["poly_w"],
        k=params["poly_k"]
    )
    
    # open output files
    handle_out = {}
    for name in ["output_fusion", "output_truncated", "output_full_length"]:
        cls = {
            "output_fusion": "fusion",
            "output_truncated": "truncated",
            "output_full_length": "full-length"
        }[name]
        # output passed
        if params[name] == "-":
            handle_out[(cls, "passed")] = sys.stdout
        elif params[name]:
            # open new file (truncate if already exist)
            handle_out[(cls, "passed")] = openg(Path(f".batch{batch_id:03d}." + params[name]), "w")
        else:
            handle_out[(cls, "passed")] = None

        # output filtered
        if params[name] and params["suffix_filtered"]:
            # open new file (truncate if already exist)
            fout = Path(params[name])
            fout = f".batch{batch_id:03d}." + fout.stem + "_" + params["suffix_filtered"] + fout.suffix
            handle_out[(cls, "filtered")] = openg(fout, "w")
        else:
            handle_out[(cls, "filtered")] = None


    
    # stream processing
    for rname in rnames:
        # get read by name
        read = indexed_fq.get(rname)
        
        # add read count
        report_dict["total reads"] += 1

        # skip too-short reads if `skip_short`
        if params["skip_short"] > len(read):
            report_dict["skipped"] += 1
            continue

        # skip low-quality reads if `skip_lowq` 
        if params["skip_lowq"] > SeqFastq.meanq(read):
            report_dict["skipped"] += 1
            continue

        PASS = "passed"
        # annotate reads
        if not params["disable_annot"]:
            annotator.annotate(read)

        # try trimming
        if params["trim_poly"]:
            Processor.trimmer(read, True, True)
        elif params["trim_adapter"]:
            Processor.trimmer(read, False, True)

        # orient read
        if params["orientation"] != 0:
            Processor.orientor(read, to=params["orientation"])

        # check length
        if params["filter_short"] > len(read):
            PASS = "filtered"

        # check quality
        if params["filter_lowq"] > SeqFastq.meanq(read):
            PASS = "filtered"
        
        # classify reads into one of: fusion/full-length/truncated
        CLASS = None
        if read.annot.fusion:
            CLASS = "fusion"
        elif read.annot.full_length:
            CLASS = "full-length"
        else:
            CLASS = "truncated"
        
        # write to file if output specified
        if handle_out[(CLASS, PASS)]:
            FastqIO.write(handle_out[(CLASS, PASS)], read)

        # update report_dict
        report_dict[CLASS][PASS] += 1


    



if __name__ == "__main__":
    
    # initiate report dict
    report_dict = {
        "start time": datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
        "total reads": 0,
        "skipped": 0,
        "fusion": {
            "passed": 0,
            "filtered": 0
        },
        "truncated": {
            "passed": 0,
            "filtered": 0
        },
        "full-length": {
            "passed": 0,
            "filtered": 0
        },
        "stop time": None,
        "params": params
    }
    main()
    
    # get the stopping time 
    report_dict["stop time"] = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


    # output report.json
    if params["report"]:
        with openg(Path(params["report"]), "w") as handle:
            handle.write(json.dumps(report_dict, indent=4))
