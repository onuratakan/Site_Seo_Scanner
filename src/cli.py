import sys
import argparse

from site_seo_scanner import site_seo_scanner

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--domain', type=str, required=True,
                        help='Domain')

    parser.add_argument('-s', '--ssl', action='store_true',
                        help='HTTPS')
    
    parser.add_argument('-sm', '--sitemap', action='store_true',
                        help='Use site map')

    parser.add_argument('-p', '--pdf', action='store_true',
                        help='Export as pdf')

    args = parser.parse_args()


    if len(sys.argv) < 2:
        parser.print_help()


    the_site_seo_scanner = site_seo_scanner(args.domain, args.ssl, args.sitemap)
    the_site_seo_scanner.print_results()

    if args.pdf:
        the_site_seo_scanner.export_pdf_results()
    

if __name__ == "__main__":
    arguments()