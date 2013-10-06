# -*- coding: utf-8 -*-

import os
import csv
import pygal
import commands
import logging
import argparse
from obd2lib.elmdecoder import decode_answer
from obd2lib.elmdb import ELMdb
from obd2lib.utils import slugify


class Graphic(object):

    def __init__(self, finput):
        self.finput = finput

        self.graphic_commands = [
            '0104',
            '0105',
            '010A',
            '010B',
            '010C',
            '010D',
            '010E',
            '0110',
            '0111',
            ]

    def parse_data(self):
        self.data = {}

        for filelog in self.finput:
            logging.info('Parsing "%s" file...', filelog)
            with open(filelog, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    # command, answer, valid, timestamp
                    command, answer, valid, timestamp = row
                    if valid == 'Y':
                        value, unit = decode_answer(command, answer)
                        d = {
                            'answer': value,
                            'timestamp': timestamp,
                            }
                        if command in self.data:
                            self.data[command].append(d)
                        else:
                            self.data[command] = [d]
                    else:
                        # skip this invalid answer
                        pass

        logging.info('Parsing done!')

    def create_graph(self):
        self.svg_foutput = []

        logging.info('Creating graphics...')
        # TODO: limitate to just relevant commands
        for command in self.data:
            if command not in self.graphic_commands:
                continue

            description = ELMdb[command]['description']
            chart = pygal.Line()
            chart.title = description

            chart.add('', [d['answer'] for d in self.data[command]])
            foutput = '{0}.svg'.format(slugify(description))
            self.svg_foutput.append(foutput)
            chart.render_to_file(foutput)
            logging.debug('Graphic for "%s" done', description)
        logging.info('All graphics created successfully')

    def convert_to_png(self):
        cmd = commands.getoutput('which inkscape')
        if cmd == '':
            logging.error('inkscape command not found')
            return

        logging.info('Converting .svg to .png...')
        for fsvg in self.svg_foutput:
            fpng = '{0}.png'.format(os.path.splitext(fsvg)[0])
            logging.debug('Converting "%s" to "%s"', fsvg, fpng)
            commands.getoutput(
                '{0} -z -e {1} -w 1024 -h 768 {2}'
                .format(cmd, fpng, fsvg))
        logging.info('All graphics converted successfully')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Parse information collected by '
        '"collect_data.py" and create some nice graphics')
    parser.add_argument(
        'inputfile', nargs='+',
        help='logfile with the data')
    parser.add_argument(
        '-p', '--convert-to-png', action="store_true",
        help='convert .svg output to .png (requires inkscape)')
    parser.add_argument(
        '-v', '--verbose', action="store_true",
        help='show logging.DEBUG into stdout')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
            level=logging.DEBUG)

    graphic = Graphic(args.inputfile)
    graphic.parse_data()
    graphic.create_graph()

    if args.convert_to_png:
        graphic.convert_to_png()
