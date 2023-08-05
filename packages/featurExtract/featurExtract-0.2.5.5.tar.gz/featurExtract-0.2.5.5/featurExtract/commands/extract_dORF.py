# -*- coding: utf-8 -*-
import sys
import gffutils
import pandas as pd 
from tqdm import tqdm 
from Bio.Seq import Seq
from collections import defaultdict
from featurExtract.utils.util import utr3_type, utr5_type, mRNA_type
from featurExtract.utils.util import stop_codon_seq, add_stop_codon 
from featurExtract.commands.extract_uORF import GFF
from featurExtract.utils.visualize import visual_transcript, visual_transcript_genome

# table header 
_dORF_csv_header = ['TranscriptID', 'Chrom', 'Strand', \
                    'CDS Interval', 'uORF Start', 'uORF End', \
                    'uORF Type', 'uORF Length', 'uORF']



class dORF(object):
    """dORF finder using object-oriented
    Attributes:
        transcript_id (str): transcript id
        chorm (str): chromosome id 
        strand (str): transcript strand 
        matural_transcript (Seq of Biopython): matural transcript sequence
        coding_sequence (Seq of Biopython): conding sequence of specifity transcript 
    """
    START_CODON = 'ATG'
    STOP_CODON_LIST = ['TAA','TAG','TGA']
    
    def __init__(self, transcript_id, chrom, strand, matural_transcript, coding_sequence):
        self.t_id = transcript_id
        self.chrom = chrom
        self.strand = strand 
        self.mt = matural_transcript
        self.cds = coding_sequence
    def transcript_location(self):
        """Transcript start and end
        1D list regradless of strand  
        """
        return [0,len(self.mt)]
    def cds_location_transcript(self):
        """Extract the cds start and end in transcript
        1D list regardless of strand 
        """
        start_codon_position = self.mt.index(self.cds)
        cds_start = start_codon_position + 1
        cds_end = start_codon_position + len(self.cds)
        return [cds_start, cds_end]

    def dorf_location_transcript(self):
        """Extract dorfs start and end in transcript
        2D list regardless strand 
        """
        d2 = []
        dORF_dict = self.dorf_parse()
        for dorf_type in dORF_dict.keys():
            for it in dORF_dict[dorf_type]:
                dorf_start, dorf_end = it[4], it[5]
                d2.append([dorf_start, dorf_end])
        return d2
    def dorf_parse(self):
        """ dORF parse"""
        dORF_dict = defaultdict(list)
        # start_codon means the first base position in matural_transcript
        start_codon = self.mt.index(self.cds)
        # stop_codon means the last base position in matural transcript
        cds_len = len(self.cds)
        stop_codon = start_codon + cds_len
        cds_intervel = str(start_codon) + '-' + str(stop_codon)
        mt_len = len(self.mt)
        utr5 = self.mt[:start_codon]
        utr5_len = len(utr5)
        utr3 = self.mt[stop_codon:]
        utr3_len = len(utr3)
        for i in range(0, utr3_len-3):
            # start codon find 
            if utr3[i:i+3] == dORF.START_CODON:
                for j in range(i+3, utr3_len, 3):
                # stop codon find
                    if utr3[j:j+3] in dORF.STOP_CODON_LIST:
                        # type1 uORF  upstream; not unique 
                        dorf = utr3[i:j+3]
                        out1 = [self.t_id, self.chrom, self.strand, cds_intervel, stop_codon+i+1, stop_codon+j+3, 'dORF', len(dorf), dorf]
                        if not dORF_dict.get('dORF'):
                            dORF_dict['dORF'] = [out1]
                        else:
                            dORF_dict['dORF'].append(out1)
                        break
        return dORF_dict
     
def uorf_procedure_oriented(transcript_id, chrom, strand, matural_transcript, coding_sequence):
    """
    Parameters:
        transcript_id:      transcript id
        matural_transcript: a Seq type (Biopython) from mature transcript without intron
        coding_sequence:    a Seq type (Biopython) from coding sequence start with ATG , 
                         end with TAA, TGA, TAG
    Return:
        down stream open reading frame in utr3
    """
    dORF_dict = defaultdict(list)
    stop_codon_list = ['TAA','TAG','TGA']
    # start_codon means the first base position in matural_transcript
    start_codon = matural_transcript.index(coding_sequence)
    # stop_codon means the last base position in matural transcript
    cds_len = len(coding_sequence)
    stop_codon = start_codon + cds_len
    cds_intervel = str(start_codon) + '-' + str(stop_codon)
    mt_len = len(matural_transcript)
    utr5 = matural_transcript[:start_codon]
    utr5_len = len(utr5)
    utr3 = matural_transcript[stop_codon:]
    utr3_len = len(utr3)
    for i in range(0, utr3_len-3):
        # start codon find 
        if utr3[i:i+3] == "ATG":
            for j in range(i+3, utr3_len, 3):
            # stop codon find
                if utr3[j:j+3] in stop_codon_list:
                    # type1 uORF  upstream; not unique 
                    dORF = utr3[i:j+3]
                    out1 = [transcript_id, chrom, strand, cds_intervel, stop_codon+i+1, stop_codon+j+3, 'dORF', len(dORF), dORF]
                    if not dORF_dict.get('dORF'):
                        dORF_dict['dORF'] = [out1]
                    else:
                        dORF_dict['dORF'].append(out1)
                    break 
    return dORF_dict




def get_dorf(args):
    """
    parameters:
        args: parse from argparse
    return:
        elements write to a file or stdout 
    """
    db = gffutils.FeatureDB(args.database, keep_order=True) # load database
    # csv
    # dORF_seq = pd.DataFrame(columns=_dORF_csv_header)
    dORF_seq_list = []
    # gff
    dORF_gff = open(args.output,'w')
    # fasta
    dorf_record = []

    mRNA_str = mRNA_type(args.style)
    index = 0
    if not args.transcript:
        for t in tqdm(db.features_of_type(mRNA_str, order_by='start'), \
                      total = len(list(db.features_of_type(mRNA_str, order_by='start'))), \
                      ncols = 80, desc = "dORF Processing:"):
            # primary transcript (pt) 是基因组上的转录本的序列，
            # 有的会包括intron，所以提取的序列和matural transcript 不一致
            # print(t)
            pt = t.sequence(args.genome, use_strand=True)
            # matural transcript (mt)
            # exon 提取的是转录本内成熟的MRNA的序列,即外显子收尾相连的matural transcript
            mt = ''
            exons_list = []
            for e in db.children(t, featuretype='exon', order_by='start'):
                exons_list.append([e.start, e.end])
                s = e.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                mt += s
            mt = Seq(mt)
            if t.strand == '-':
                mt = mt.reverse_complement()
            # CDS 提取的是编码区 ATG ... TAG
            cds = ''
            for c in db.children(t, featuretype='CDS', order_by='start'):
                # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                s = c.sequence(args.genome, use_strand=False)
                cds += s
            if args.style == 'GTF':
                sc_seq = stop_codon_seq(db, t, args.genome)
                cds = add_stop_codon(cds, t.strand, sc_seq)
            cds = Seq(cds)
            if t.strand == '-':
                cds = cds.reverse_complement()
            dORF_dict = uorf_procedure_oriented(t.id, t.chrom, t.strand, mt, cds)
            # loop all dORF
            for key in sorted(dORF_dict.keys()):
                for it in dORF_dict[key]:
                    # csv output format 
                    if args.output_format == 'csv':
                        # dORF_seq.loc[index] = it
                        # index += 1
                        dORF_seq_list.append(dict((_dORF_csv_header[i],it[i]) for i in range(len(_dORF_csv_header))))
                    elif args.output_format == 'fasta':
                        dorf_id = ".".join(map(str,[it[0], it[4], it[5], it[6]]))
                        seq = it[8] # it[8] is a Seq type
                        desc='strand:%s uORF=%d-%d %s length=%d CDS=%s-%s'%(it[2],
                                                                        it[4],
                                                                        it[5],
                                                                        it[6],
                                                                        len(seq),
                                                                        it[3].split('-')[0],
                                                                        it[3].split('-')[1])
                        dorfRecord = SeqRecord(seq, id=dorf_id.replace('transcript:',''), description=desc)
                        dorf_record.append(dorfRecord)
                    elif args.output_format == 'gff':
                        gff = GFF(exons_list, it, 'dORF')
                        dorf_gff_line,features_gff_lines = gff.parse()
                        ex_locations = gff.uorf_exons_location()
                        dORF_gff.write(dorf_gff_line+"\n")
                        for feature_line in features_gff_lines:
                            dORF_gff.write(feature_line+"\n")
        if args.output_format == 'csv':
            dORF_seq = pd.DataFrame.from_dict(dORF_seq_list)
            dORF_seq.to_csv(args.output, sep=',', index=False)
        elif args.output_format == 'gff':
            dORF_gff.close()
        elif args.output_format == 'fasta':
            with open(args.output,'w') as handle:
                SeqIO.write(uorf_record, handle, "fasta")
    else:
        for t in db.features_of_type(mRNA_str, order_by='start'):
            # primary transcript (pt) 是基因组上的转录本的序列，
            # 有的会包括intron，所以提取的序列和matural transcript 不一致
            # print(t)
            if args.transcript in t.id:
                pt = t.sequence(args.genome, use_strand=True)
                # matural transcript (mt)
                # exon 提取的是转录本内成熟的MRNA的序列,即外显子收尾相连的matural transcript
                mt = ''
                exons_list = []
                for e in db.children(t, featuretype='exon', order_by='start'):
                    exons_list.append([e.start, e.end])
                    s = e.sequence(args.genome, use_strand=False) # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                    mt += s
                mt = Seq(mt)
                if t.strand == '-':
                    mt = mt.reverse_complement()
                # CDS 提取的是编码区 ATG ... TAG
                cds = ''
                cds_list = []
                for c in db.children(t, featuretype='CDS', order_by='start'):
                    # 不反向互补，对于负链要得到全部的cds后再一次性反向互补
                    cds_list.append([c.start, c.end])
                    s = c.sequence(args.genome, use_strand=False)
                    cds += s
                if args.style == 'GTF':
                    sc_seq = stop_codon_seq(db, t, args.genome)
                    cds = add_stop_codon(cds, t.strand, sc_seq)
                cds = Seq(cds)
                if t.strand == '-':
                    cds = cds.reverse_complement()
                # precodure-oriented
                # dORF_dict = dorf(t.id, t.chrom, t.strand, mt, cds)
                dORF_ = dORF(t.id, t.chrom, t.strand, mt, cds)
                dORF_dict = dORF_.dorf_parse()
                dorf_location_genome = [] # for schematic on genome # 3D list 
                for key in sorted(dORF_dict.keys()):
                    for it in dORF_dict[key]:
                        # csv output format 
                        if args.output_format == 'csv':
                            # dORF_seq.loc[index] = it
                            # index += 1
                            dORF_seq_list.append(dict((_dORF_csv_header[i],it[i]) for i in range(len(_dORF_csv_header))))
                        elif args.output_format == 'fasta':
                            dorf_id = ".".join(map(str,[it[0], it[4], it[5], it[6]]))
                            seq = it[8] # it[8] is a Seq type
                            desc='strand:%s uORF=%d-%d %s length=%d CDS=%s-%s'%(it[2],
                                                                        it[4],
                                                                        it[5],
                                                                        it[6],
                                                                        len(seq),
                                                                        it[3].split('-')[0],
                                                                        it[3].split('-')[1])
                            dorfRecord = SeqRecord(seq, id=dorf_id.replace('transcript:',''), description=desc)
                            dorf_record.append(dorfRecord)
                        elif args.output_format == 'gff':
                            gff = GFF(exons_list, it, 'dORF')
                            dorf_gff_line,features_gff_lines = gff.parse()
                            ex_locations = gff.uorf_exons_location()
                            dorf_location_genome.append(ex_locations) # for schematic on genome
                            dORF_gff.write(dorf_gff_line+"\n")
                            for feature_line in features_gff_lines:
                                dORF_gff.write(feature_line+"\n")
                # figure the schametic 
                # without intron 
                if args.schematic_without_intron:
                    figure = visual_transcript(args.schematic_without_intron,
                                               args.transcript,
                                               dORF_.transcript_location(),
                                               dORF_.cds_location_transcript(),
                                               dORF_.dorf_location_transcript(),
                                               'dORF')
                    figure.draw()
                # with intron
                if args.schematic_with_intron:
                    figure = visual_transcript_genome(t.strand,
                                                      args.schematic_with_intron,
                                                      args.transcript,
                                                      exons_list,
                                                      cds_list,
                                                      dorf_location_genome,# 3D list 
                                                      'dORF')
                    figure.draw()
                
                if args.output_format == 'csv':
                    dORF_seq = pd.DataFrame.from_dict(dORF_seq_list)
                    dORF_seq.to_csv(args.output, sep=',', index=False)
                elif args.output_format == 'gff':
                    dORF_gff.close()
                elif args.output_format == 'fasta':
                    with open(args.output,'w') as handle:
                        SeqIO.write(uorf_record, handle, "fasta")
                break 
