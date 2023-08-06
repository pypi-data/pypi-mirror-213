# scospus

Parse PUS-type packets and interprete them using an SCOS-2000 database.

You can find the [documentation here](https://irf.developer.irf.se/scospus/).

## Requirements

This python packet depends on [pyscos2000](https://gitlab.irf.se/irf/pyscos2000).


## Installation

To install `scospus` you will have to clone the repository and install 
it like this:

    git clone https://gitlab.irf.se/irf/scospus.git
    pip install ./scospus

In case you want to actually modify this library be sure to clone the 
repository through ssh and install it in a way that’ll allow you to build 
the documentation, too:

    git clone git@gitlab.irf.se:irf/scospus.git
    pip install -e ./scospus[docs]


## Usage

Simple example of how to parse a dds file:

    from pyscos2000 import SCOS
    from scospus import PUSType
    from scospus.dds import DDSReader

    # point this to the folder with your .dat files of the SCOS database
    scos = SCOS('./mib/ASCII')

    # you can select parameters by description:
    myparam = [pcf['PCF_NAME'].value
               for pcf in scos.pcf.rows
               if pcf['PCF_DESCR'].value == 'my parameter']
    myparam = myparam[0]

    for ddspacket in DDSReader('my_tms.dds'):
        puspacket = ddspacket.payload
        assert puspacket.crc_ok()

        packet = puspacket.interprete(scos)

        if packet.pus.type != PUSType.TELEMETRY:
            # not just for show: currently no support for telecommands
            continue

        print(ddspacket.timestamp, puspacket.timestamp, packet.apid, packet.pid['PID_DESCR'].value)
        for param in packet:
            print(f' {param.description} ({param.name}): {param.eng} ({param.hex})')

        # or access the parameters directly by name
        print('   ', packet[myparam].eng)


## Uncertain source files

If you don’t know what data file you’re looking at, you might want to give 
`scospus.guess_reader` a shot: it'll try to extract one packet from the 
source file using each available reader and returns the type of reader that 
wasn’t useless:

    import scospus

    reader = scospus.guess_reader(my_file)
    if reader is None:
        print("No idea")
    else:
        for packet in reader(my_file):
            # the usual


## Timestamp correction / epoch handling

The epoch is assumed to be 1970-01-01, but you can set it to whatever your 
epoch is. In the example the epoch is set to 1992-04-13 11:16:05 (because 
why not):

    import datetime

    import scospus.pus

    scospus.pus.EPOCH = datetime.datetime(1992, 4, 13, 11, 16, 5)


## License

[MIT](LICENSE)
