#!python

"""
Generate final annotated, soft-filtered Matrix Table
"""

import logging
import click
import hail as hl

from joint_calling.utils import get_validation_callback, get_mt, file_exists
from joint_calling import utils, _version

logger = logging.getLogger('joint-calling')
logger.setLevel('INFO')


@click.command()
@click.version_option(_version.__version__)
@click.option(
    '--mt',
    'mt_path',
    required=True,
    callback=get_validation_callback(ext='mt', must_exist=True),
    help='path to the input raw Matrix Table, generated by combine_gvcfs.py',
)
@click.option(
    '--out-mt',
    'out_mt_path',
    required=True,
    callback=get_validation_callback(ext='mt', must_exist=False),
    help='path to write the final annotated soft-filtered Matrix Table',
)
@click.option(
    '--meta-ht',
    'meta_ht_path',
    required=True,
    help='Table generated by sample_qc.py',
)
@click.option(
    '--var-qc-final-filter-ht',
    'var_qc_final_filter_ht_path',
    required=True,
    help='Table with AS-VQSR annotations',
)
@click.option(
    '--local-tmp-dir',
    'local_tmp_dir',
    help='local directory for temporary files and Hail logs (must be local).',
)
@click.option(
    '--overwrite/--reuse',
    'overwrite',
    is_flag=True,
    help='if an intermediate or a final file exists, skip running the code '
    'that generates it.',
)
@click.option(
    '--hail-billing',
    'hail_billing',
    help='Hail billing account ID.',
)
def main(
    mt_path: str,
    out_mt_path: str,
    meta_ht_path: str,
    var_qc_final_filter_ht_path: str,
    local_tmp_dir: str,
    overwrite: bool,  # pylint: disable=unused-argument
    hail_billing: str,  # pylint: disable=unused-argument
):
    """
    Generate final annotated, soft-filtered Matrix Table
    """
    utils.init_hail('make_finalised_mt', local_tmp_dir)

    if file_exists(out_mt_path):
        if overwrite:
            logger.info(f'Output {out_mt_path} exists and will be overwritten')
        else:
            logger.error(
                f'Output file {out_mt_path} exists, use --overwrite to overwrite'
            )
            return

    mt = get_mt(
        mt_path,
        split=True,
        meta_ht=hl.read_table(meta_ht_path),
        add_meta=True,
    )

    var_qc_ht = hl.read_table(var_qc_final_filter_ht_path)
    mt = mt.annotate_rows(**var_qc_ht[mt.row_key])
    mt = mt.annotate_globals(**var_qc_ht.index_globals())
    mt.write(out_mt_path, overwrite=True)


if __name__ == '__main__':
    main()  # pylint: disable=E1120
