#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : generate.py
# License           : MIT license <Check LICENSE>
# Author            : Anderson Ignacio da Silva (aignacio) <anderson@aignacio.com>
# Date              : 20.02.2023
# Last Modified Date: 12.06.2023
import logging
import os
import sys
import shutil
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

try:
    from ipsocgen.common.constants import options,base_module
    from ipsocgen.common.modules import *
except ImportError:
    from common.constants import options,base_module
    from common.modules import *

def mpsoc_gen(mpsoc, mpsoc_name, desc, output, mmap):
    mpsoc_hdl_obj = []

    # Get all SoC IOs
    socs_list = []
    n_of_tiles = 0
    for tile_id, tile_dic in mpsoc['tiles'].items():
        n_of_tiles = tile_id
        socs_list.append(soc_gen(tile_dic,
                                 'tile_'+str(tile_id),
                                 'MPSoC tile no '+str(tile_id),
                                 output,
                                 mmap, True if tile_id == 0 else False))

    # Clocks and resets
    mpsoc_cfg = {}
    mpsoc_cfg['clk'] = mpsoc['clk']['clk_int']
    mpsoc_cfg['rst'] = mpsoc['rst']['rst_int']
    mpsoc_cfg['txn_id'] = 8

    mpsoc_hdl_obj.append(Clock(mpsoc))
    mpsoc_hdl_obj.append(Reset(mpsoc))
    io, in_s, out_s = _soc_io(mpsoc_hdl_obj)

    # RTL object generation
    # Generate module header with its defines
    global_rtl = ModuleHeader('mpsoc',
                              mpsoc_name,
                              desc,
                              io).get_hdl()

    # Signals to be first declared
    # Extract the signals and add to the RTL
    for obj in mpsoc_hdl_obj:
        for ip in obj.get_signals():
            global_rtl += ip
            global_rtl += '\n'

    global_rtl += '  s_axi_mosi_t [`NUM_TILES-1:0] slaves_axi_mosi;\n'
    global_rtl += '  s_axi_mosi_t [`NUM_TILES-1:0] ravenoc_mosi;\n'
    global_rtl += '  s_axi_miso_t [`NUM_TILES-1:0] slaves_axi_miso;\n'
    global_rtl += '  s_axi_miso_t [`NUM_TILES-1:0] ravenoc_miso;\n'
    global_rtl += '  s_irq_ni_t   [`NUM_TILES-1:0] irqs_ravenoc;\n'
    global_rtl += '  logic '+mpsoc_cfg['rst']+';\n\n'

    # Add the RTL modules of Clock / Reset
    for obj in mpsoc_hdl_obj:
        global_rtl += obj.get_hdl()

    # Instantiate each SoC looking for its clock/reset inputs
    module_info = {}
    module_info['io_clk_mpsoc'] = mpsoc_cfg['clk']
    module_info['io_rst_mpsoc'] = mpsoc_cfg['rst']

    for index, soc in enumerate(socs_list):
        module_info['name'] = soc['name']
        module_info['io_noc_miso'] = 'slaves_axi_mosi['+str(index)+']'
        module_info['io_noc_mosi'] = 'slaves_axi_miso['+str(index)+']'
        module_info['io_noc_irq']  = 'irqs_ravenoc['+str(index)+']'
        module_info['io_clk'] = soc['clk_ext']
        module_info['io_rst'] = soc['rst_ext']
        global_rtl += ModuleInstance(module_info).get_hdl()

    global_rtl += RaveNoC(mpsoc['noc'], mpsoc_cfg, 0, 'instance').get_hdl()
    global_rtl += '\nendmodule'

    _gen_design_files(mpsoc_name, global_rtl, mpsoc_hdl_obj, output)

    ##### DEFINES #####
    # Create the configuration file
    # For MPSoC, use default default definitions for bus+dma
    # TODO: update to use parameters in all IPs instead of macros

    defines = ModuleDefines(mpsoc_name,
                            'mpsoc',
                            'Verilog defines configuration file',
                            _gen_defines_mpsoc(mpsoc['noc'], socs_list[0]['noc_base_addr']))
    _gen_design_files(mpsoc_name+'_defines', defines.get_hdl(), [defines], output)


def soc_gen(soc, soc_name, desc, output, mmap, gen_defines):
    logging.debug('Starting to generate files for SoC - '+soc_name)

    mst = soc['masters']
    slv = soc['slaves']

    soc_cfg = {}
    soc_cfg['clk']     = soc['clk']['clk_int']
    soc_cfg['rst']     = soc['rst']['rst_int']
    soc_cfg['clk_ext'] = soc['clk']['io_in_clk']
    soc_cfg['rst_ext'] = soc['rst']['io_in_rst']
    soc_cfg['txn_id']  = soc['txn_id_width']

    pll = {}
    dma_info = {}
    hdl_obj = []

    # Clocks and resets first
    hdl_obj.append(Clock(soc))
    hdl_obj.append(Reset(soc))

    # Crossbar
    bus = Axi4Bus(soc, mmap)
    hdl_obj.append(bus)

    # Masters
    for master in _soc_master(bus, soc, soc_cfg, dma_info):
        hdl_obj.append(master)

    # Slaves
    for slave in _soc_slaves(bus, soc, soc_cfg, dma_info):
        hdl_obj.append(slave)

    # RTL object generation
    global_rtl = ''

    # Module Header
    io, in_s, out_s = _soc_io(hdl_obj)
    global_rtl += ModuleHeader('soc', soc_name, desc, io).get_hdl()

    # Signals to be first declared
    for obj in hdl_obj:
        for ip in obj.get_signals():
            global_rtl += ip
            global_rtl += '\n'
    global_rtl += '\n'

    # Get the RTL modules
    for obj in hdl_obj:
        global_rtl += obj.get_hdl()

    global_rtl += '\nendmodule'

    logging.debug('Generating RTL for SoC - '+soc_name)
    _gen_design_files(soc_name, global_rtl, hdl_obj, output)
    logging.debug('Generating header C files for SoC - '+soc_name)
    _gen_header_files(soc_name, bus, hdl_obj, output)

    soc_data = {}
    soc_data['name'] = soc_name
    soc_data['input'] = in_s
    soc_data['output'] = out_s
    soc_data['clk_ext'] = soc['clk']['io_in_clk']
    soc_data['rst_ext'] = soc['rst']['io_in_rst']
    soc_data['noc_base_addr'] = bus.get_noc_addr()

    ##### DEFINES #####
    # Create the configuration file
    defines_list = []

    if gen_defines == True:
        # Masters
        for master_or_slaves in hdl_obj:
            defines_list.append(master_or_slaves.get_defines())
        defines = ModuleDefines(soc_name,
                               'soc',
                               'Verilog defines configuration file',
                               defines_list)
        _gen_design_files(soc_name+'_defines', defines.get_hdl(), [defines], output)

    logging.info('All files sucessfully generated for SoC - '+soc_name)
    return soc_data

def _gen_design_files(soc_name, global_rtl, hdl_obj, out_dir):
    types = set()
    # Creates a set without repeated acc types
    for obj in hdl_obj:
        types.add(obj.get_acc_type())

    out_rtl = os.path.join(out_dir,'rtl')

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        logging.debug('Creating output directory: '+str(out_dir))
    if not os.path.exists(out_rtl):
        os.mkdir(out_rtl)
        logging.debug('Creating RTL directory: '+str(out_rtl))

    rtl_out = os.path.join(out_rtl,soc_name+'.sv')
    soc_rtl = open(rtl_out, "w")
    soc_rtl.write(global_rtl)
    soc_rtl.close()

def _gen_header_files(soc_name, bus, hdl_obj, out_dir):
    types = set()
    # Creates a set without repeated acc types
    for obj in hdl_obj:
        types.add(obj.get_acc_type())

    out_sw = os.path.join(out_dir,'sw')

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
        logging.debug('Creating output directory: '+str(out_dir))
    if not os.path.exists(out_sw):
        os.mkdir(out_sw)
        logging.debug('Creating SW directory: '+str(out_sw))

    header_out = os.path.join(out_sw, soc_name+'.h')
    header_file = open(header_out, "w")
    header_file.write('#ifndef '+soc_name.upper()+'_H')
    header_file.write('\n#define '+soc_name.upper()+'_H')
    header_file.write('\n\n')
    header_file.write('// AUTO-GENERATED header file through IPSoCGen')
    header_file.write('\n// '+datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    header_file.write('\n\n')
    header_file.write(tabulate(bus.table_masters_c, tablefmt="plain"))
    header_file.write('\n\n')
    header_file.write(tabulate(bus.table_slaves_c, tablefmt="plain"))
    header_file.write('\n\n')

    table = []
    for slave in range(len(bus.description)):
        slave_info = _fmt_base_addr(bus.description[slave], bus.base_addr_h[slave])
        table.append(['#define', slave_info['desc'], '0x'+slave_info['baddr']])
    header_file.write(tabulate(table, ['//', 'SLAVE', 'BASE ADDRESS'], tablefmt='plain'))
    header_file.write('\n\n')

    table = []
    for slave in range(len(bus.description)):
        slave_info_mem_size = _fmt_mem_size(bus.description[slave], bus.mem_size[slave])
        #table.append(['#define', slave_info_mem_size['desc'], slave_info_mem_size['mem'], slave_info_mem_size['mem_kib']])
        table.append(['#define', slave_info_mem_size['desc'], slave_info_mem_size['mem']])
    #header_file.write(tabulate(table, ['//', 'SLAVE', 'MEM SIZE BYTES','SIZE KiB'], tablefmt='plain'))
    header_file.write(tabulate(table, ['//', 'SLAVE', 'MEM SIZE BYTES'], tablefmt='plain'))
    header_file.write('\n')

    header_file.write('\n#endif')
    header_file.close()

def _fmt_base_addr(description, base_address):
    info  = {}
    desc  = str(description).replace(' ','_')+'_BASE_ADDR'
    info['desc']  = desc.upper()
    info['baddr'] = str(base_address)
    return info

def _fmt_mem_size(description, mem_size):
    info  = {}
    desc  = str(description).replace(' ','_')+'_SIZE'
    info['desc']  = desc.upper()
    info['mem'] = str(mem_size*1024)
    info['mem_kib'] = '// '+str(mem_size)+'KiB'
    return info

def _soc_slaves(bus, soc, soc_cfg, dma_info):
    hdl_obj = []
    mmap = bus.get_mmap()
    eth_info = {}
    eth_info['if'] = 0

    for slave, slave_desc in soc['slaves'].items():
        if slave_desc['type'] == 'ram_mem':
            iram = Axi4MemRAM(slave_desc, soc_cfg, slave)
            hdl_obj.append(iram)
        elif slave_desc['type'] == 'rom_mem':
            irom = Axi4MemROM(slave_desc, soc_cfg, slave)
            hdl_obj.append(irom)
        elif slave_desc['type'] == 'acc_dma':
            master = dma_info[slave_desc['name']]
            dma = Axi4DMA(slave_desc, soc_cfg, slave, master)
            hdl_obj.append(dma)
        elif slave_desc['type'] == 'acc_uart':
            uart = Axi4UART(slave_desc, soc_cfg, slave)
            hdl_obj.append(uart)
        elif slave_desc['type'] == 'acc_irq':
            irq_ctrl = Axi4Irq(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(irq_ctrl)
        elif slave_desc['type'] == 'acc_timer':
            timer = Axi4Timer(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(timer)
        elif slave_desc['type'] == 'acc_custom_slave':
            custom = Axi4AccCustomSlave(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(custom)
        elif slave_desc['type'] == 'acc_rst':
            rst = Axi4RstCtrl(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(rst)
        elif slave_desc['type'] == 'acc_noc':
            noc = RaveNoC(slave_desc, soc_cfg, slave, 'slave')
            hdl_obj.append(noc)
        elif slave_desc['type'] == 'acc_eth':
            eth_info['if'] += 1
            if slave_desc['eth_type'] == 'csr':
                eth_info['name']                = slave_desc['name']
                eth_info['clk_ext']             = slave_desc['clk_ext']
                eth_info['desc']                = slave_desc['desc']
                eth_info['csr_slv_id']          = slave
                eth_info.update(slave_desc)
            elif slave_desc['eth_type'] == 'infifo':
                eth_info['inf_slv_id'] = slave
            elif slave_desc['eth_type'] == 'outfifo':
                eth_info['out_slv_id'] = slave

            if eth_info['if'] == 3:
                eth = Axi4AccEthernet(soc_cfg, eth_info)
                hdl_obj.append(eth)
        else:
            logging.warning('Unknown slave - '+slave_desc['type'])
    return hdl_obj

def _soc_master(bus, soc, soc_cfg, dma_info):
    hdl_obj = []
    cpu_included = 0
    nox_cpu_included = 0
    vex_cpu_included = 0

    for master, master_desc in soc['masters'].items():
        if master_desc['type'] == 'cpu_nox':
            nox_cpu_included = 1
            if vex_cpu_included == 1:
                logging.error('Multiple CPUs included in master list!')
                sys.exit(1)
            if cpu_included == 0:
                cpu_included = 1
                hdl_obj.append(RISCVCpu(soc, bus.get_mmap(), 'nox'))
        elif master_desc['type'] == 'cpu_vex':
            vex_cpu_included = 1
            if nox_cpu_included == 1:
                logging.error('Multiple CPUs included in master list!')
                sys.exit(1)
            if cpu_included == 0:
                cpu_included = 1
                hdl_obj.append(RISCVCpu(soc, bus.get_mmap(), 'vex'))
        elif master_desc['type'] == 'acc_dma':
            dma_info[master_desc['name']] = master
            logging.debug('Master '+master_desc['type']+
                          ' will be added later in the slave side')
        elif master_desc['type'] == 'acc_custom_master':
            custom = Axi4AccCustomMaster(master_desc, soc_cfg, master)
            hdl_obj.append(custom)
        else:
            logging.warning('Unknown master type! - '+master_desc['type'])
    if cpu_included == 0 and soc['proc_required'] == 'y':
        logging.error('CPU not included in masters!')
        sys.exit(1)
    return hdl_obj

def _soc_io(hdl_obj):
    io_list = []
    input_signals = []
    output_signals = []
    for obj in hdl_obj:
        input_s = obj.get_io()['in']
        output_s = obj.get_io()['out']
        for i in input_s:
            if i not in input_signals:
                input_signals.append(i)
        for j in output_s:
            if j not in output_signals:
                output_signals.append(j)

    for i in range(len(input_signals)):
        tmp = 'input\t\t'+input_signals[i][0]+'\t'+input_signals[i][1]
        io_list.append(tmp)
    for i in range(len(output_signals)):
        tmp = 'output\t'+output_signals[i][0]+'\t'+output_signals[i][1]
        io_list.append(tmp)

    return io_list, input_signals, output_signals

def _gen_defines_mpsoc(noc, base_addr):
    defines = []

    noc_defines = {}
    noc_defines['flit_buff']            = noc['flit_buff']
    noc_defines['flit_data_width']      = noc['flit_data_width']
    noc_defines['h_priority']           = str(noc['h_priority'])
    noc_defines['routing_alg']          = str(noc['routing_alg'])
    noc_defines['max_sz_pkt']           = str(noc['max_sz_pkt'])
    noc_defines['noc_cfg_sz_rows']      = str(noc['size_x'])
    noc_defines['noc_cfg_sz_cols']      = str(noc['size_y'])
    noc_defines['ravenoc_base_addr']    = '\'h'+str(base_addr)
    noc_defines['n_virt_chn']           = str(noc['n_virt_chn'])
    noc_defines['rd_axi_bff(x)']        = 'x<=2?2:4'
    noc_defines['num_tiles']            = str(noc['size_x']*noc['size_y'])
    noc_defines['axi_wr_bff_base_addr'] = '`RAVENOC_BASE_ADDR+\'h1000'
    noc_defines['axi_rd_bff_base_addr'] = '`RAVENOC_BASE_ADDR+\'h2000'
    noc_defines['axi_csr_base_addr']    = '`RAVENOC_BASE_ADDR+\'h3000'
    noc_defines['axi_max_outstd_rd']    = 2
    noc_defines['axi_max_outstd_wr']    = 2

    defines.append(noc_defines)
    return defines
