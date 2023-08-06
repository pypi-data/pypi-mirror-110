import dnaio
import pandas as pd
import argparse


def rev_c(seq):
    """
    simple function that reverse complements a given sequence
    """
    tab = str.maketrans("ACTGN", "TGACN")
    # first reverse the sequence
    seq = seq[::-1]
    # and then complement
    seq = seq.translate(tab)
    return seq


def read_fasta(filename):
    """
    This is a simple function written in base python that
    returns a dictionary made from a fasta file
    """
    # Read in the transcript fasta
    fasta = {}
    with open(filename, 'r') as file:
        for line in file:
            if line.rstrip()[0:1] == ">":
                this_tx_name = line.rstrip().replace(">", "")
            else:
                try:
                    fasta[this_tx_name] += line.rstrip()
                except KeyError:
                    fasta[this_tx_name] = line.rstrip()
    return fasta


def find_guides(seq):
    gg_pos = [i for i, s in enumerate(seq) if seq[i:i + 2] == "GG" and i >= 21]  # not 22, because 0 based
    guides = []
    for i in gg_pos:
        guides.append(seq[i - 21:i - 1])
    return guides


def gen_guide_df(fastq_file, min_rl, max_rl, max_reads, max_guides, T7, overlap):
    seqs = {}  # records which sequences are in fastq, with copy numbers
    guides_d = {}  # how many reads are targeted by each guide
    seq_guide_match = {}  # which guides match the given sequence
    total_reads = 0
    counter = 0

    # make a dictionary of each read sequence and how many copies of it we have
    with dnaio.open(fastq_file) as f:
        for record in f:
            if min_rl < len(record.sequence) < max_rl:
                counter += 1
                try:
                    seqs[record.sequence] += 1
                except KeyError:
                    seqs[record.sequence] = 1

                total_reads += 1

                if counter >= max_reads > 0:
                    stopped_early = True
                    break

    # Generate all possible guides for all possible sequences
    for seq, copy_no in seqs.items():
        this_guides = find_guides(seq) + find_guides(rev_c(seq))

        # work out how many reads each guide will target
        for guide in this_guides:
            try:
                guides_d[guide] += copy_no
            except KeyError:
                guides_d[guide] = copy_no

        # save which guides target each sequence
        seq_guide_match[seq] = this_guides

    # now sort this list
    sorted_guides = {k: v for k, v in sorted(guides_d.items(), key=lambda item: item[1], reverse=True)}

    # final list - filter for guides that target the most sequences
    final_guides = {}
    counter = 0
    for guide, copy_no in sorted_guides.items():
        counter += 1
        if counter > max_guides:
            break
        else:
            final_guides[guide] = copy_no

    # now find how many sequences are actually targeted (can't do this just by looking at the final_guide df as
    # some sequences will be targeted by multiple guides, so would be counted twice or more)

    n = 0  # total reads which are targeted
    guide_fraction = {}  # what fraction of the library each guide targets
    for seq, copy_no in seqs.items():
        # find the guides associated with this seq
        this_guides = seq_guide_match[seq]

        # check if any are in the list of final guides
        combined_set = set(this_guides).intersection(final_guides.keys())
        if len(combined_set) > 0:
            n += copy_no

            # find what fraction of the library each guide targets
            for guide in combined_set:
                try:
                    guide_fraction[guide] += copy_no / total_reads
                except KeyError:
                    guide_fraction[guide] = copy_no / total_reads

    total_percent = round(100 * n / total_reads, 2)
    print(str(total_percent) + "% of library targeted by guides")

    final_oligos = {}
    for guide in final_guides.keys():
        if not guide[0:1] == "G":
            final_oligos[guide] = T7 + "G" + guide + overlap
        else:
            final_oligos[guide] = T7 + guide + overlap

    final_df = {"oligo": list(final_oligos.values()), "target": list(final_oligos.keys()),
                "fraction": [guide_fraction[a] for a in final_oligos.keys()], "total_targeted": total_percent}

    df = pd.DataFrame.from_dict(final_df)
    
    # filter seqs df for abundant reads
    abundant_seqs = {}
    for seq, copy_no in seqs.items():
        if copy_no >= 0.001*total_reads:
            abundant_seqs[seq] = copy_no
    
    return df, abundant_seqs


def check_background(df, fasta_d, T7, overlap):
    """
    This function generates all the possible oligos for sgRNAs that will target the sequences in the background.

    df is a dataframe containing all the oligos we've designed
    fasta_d is a dictionary of DNA sequences
    """

    background_d = {}  # dictionary of guides and how many sequences in background are targeted
    for oligo in df["oligo"]:
        background_d[oligo] = 0  # initialise

    counter = 0
    for name, sequence in fasta_d.items():
        counter += 1
        if counter % 1_000 == 0:
            print(str(counter) + " sequences checked")

        this_guides = find_guides(sequence) + find_guides(rev_c(sequence))

        for guide in this_guides:
            if not guide[0:1] == "G":
                oligo = T7 + "G" + guide + overlap
            else:
                oligo = T7 + guide + overlap

            if oligo in background_d.keys():
                background_d[oligo] += 1
            else:
                background_d[oligo] = 1

    df["Off_targets"] = df["oligo"].map(background_d)

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs='+', default=[], required=True, help="Input fastq(s)")
    parser.add_argument("-o", "--output", type=str, required=True, help="output filename")
    parser.add_argument("-r", "--max_reads", type=int, required=False, default=-1, help="max reads to examine")
    parser.add_argument("-g", "--max_guides", type=int, required=False, default=50)
    parser.add_argument("--min_read_length", type=int, required=False, default=0)
    parser.add_argument("--max_read_length", type=int, required=False, default=1000)
    parser.add_argument("--save_stats", default=False, action="store_true")
    parser.add_argument("-b", "--background", type=str, required=False, default="None",
                        help="A fasta file of background sequences that you do not wish to target")
    parser.add_argument("--t7", default="TTCTAATACGACTCACTATA", help="T7 promoter sequence")
    parser.add_argument("--overlap", default="GTTTTAGAGCTAGA", help="The overlap, compatible with EnGen NEB kit")
    args = parser.parse_args()
    
    seqs_list = []
    
    if args.background != "None":
        print("Reading background fasta")
        fasta_d = read_fasta(filename=args.background)

    if len(args.input) == 1:
        full_df, seqs = gen_guide_df(fastq_file=args.input[0], min_rl=args.min_read_length, max_rl=args.max_read_length,
                               max_reads=args.max_reads, max_guides=args.max_guides, T7=args.t7, overlap=args.overlap)
        seqs_list.append(seqs)
    else:
        for i, filename in enumerate(args.input):
            print("Analysing " + filename)
            df, seqs = gen_guide_df(fastq_file=filename, min_rl=args.min_read_length, max_rl=args.max_read_length,
                              max_reads=args.max_reads, max_guides=args.max_guides, T7=args.t7, overlap=args.overlap)
            df["filename"] = filename.split("/")[-1]
            seqs_list.append(seqs)
            if i == 0:
                full_df = df
            else:
                full_df = full_df.append(df)
        full_df["average_fraction"] = full_df['fraction'].groupby(full_df["oligo"]).transform('sum') / len(args.input)

    if args.background != "None":
        print("Checking background")
        full_df = check_background(full_df, fasta_d, T7=args.t7, overlap=args.overlap)
        
    if args.save_stats:
        counter = 0
        for seqs, filename in zip(seqs_list, args.input):
            counter += 1
            seq_df = pd.DataFrame.from_dict({'Sequence': seqs.keys(), 'n': seqs.values(), 'name': filename})
            seq_df = seq_df.sort_values(by='n', ascending=False)
            if counter == 1:
                full_seq_df = seq_df
            else:
                full_seq_df = full_seq_df.append(seq_df)
        full_seq_df.to_csv(args.output + '.stats.csv', index=False)

    print("Saving to csv")
    full_df.to_csv(args.output+'.csv', index=False)
    print("Complete!")


if __name__ == "__main__":
    main()
