"""Subclass of MDSplus data fetcher to grab additional H1-specific metadata."""
import pyfusion
from pyfusion.acquisition.MDSPlus.fetch import MDSPlusDataFetcher, get_tree_path
import pyfusion.acquisition.MDSPlus.h1ds as mdsweb
from pyfusion.data.timeseries import TimeseriesData, Signal, Timebase
from pyfusion.data.base import Coords, Channel, ChannelList, \
    get_coords_for_channel
import traceback

class DIIIDDataFetcher(MDSPlusDataFetcher):
    """Subclass of MDSplus fetcher to get additional H1-specific metadata."""

    def do_fetch(self):
        print('hello world22')
        output_data = super(DIIIDDataFetcher, self).do_fetch()
        coords = get_coords_for_channel(**self.__dict__)
        ch = Channel(self.mds_path, coords)
        output_data.channels = ch
        output_data.meta.update({'shot':self.shot, 'kh':self.get_kh()})
        print(ch)
        output_data.config_name = ch
        return output_data

    def get_kh(self):
        # TODO: shouldn't need to worry about fetch mode here...
        imain2_path = '\h1data::top.operations.magnetsupply.lcu.setup_main.i2'
        isec2_path = '\h1data::top.operations.magnetsupply.lcu.setup_sec.i2'
        if self.fetch_mode == 'thin client':
            try:
                imain2 = self.acq.connection.get(imain2_path)
                isec2 = self.acq.connection.get(isec2_path)
                return float(isec2/imain2)
            except:
                return None
        elif self.fetch_mode == 'http':
            print("http fetch of k_h disabled until supported by H1DS")
            return -1.0
            """
            imain2_path_comp = get_tree_path(imain2_path)
            isec2_path_comp = get_tree_path(isec2_path)
            
            imain2_url = self.acq.server + '/'.join([imain2_path_comp['tree'],
                                                     str(self.shot),
                                                     imain2_path_comp['tagname'],
                                                     imain2_path_comp['nodepath']])
            isec2_url = self.acq.server + '/'.join([isec2_path_comp['tree'],
                                                    str(self.shot),
                                                    isec2_path_comp['tagname'],
                                                    isec2_path_comp['nodepath']])
            imain2 = mdsweb.data_from_url(imain2_url)
            isec2 = mdsweb.data_from_url(isec2_url)
            return float(isec2/imain2)
            """
            
        else:
            try:
                imain2 = self.tree.getNode(imain2_path)
                isec2 = self.tree.getNode(isec2_path)
                return float(isec2/imain2)
            except:
                if pyfusion.DBG() > 0: 
                    traceback.print_exc()
                return None
        

class DIIIDDataFetcherPTdata(MDSPlusDataFetcher):
    """Subclass of MDSplus fetcher to get additional H1-specific metadata."""
    def setup(self):
        print('WHAAAAAAAAAAT')
        # self.mds_path_components = get_tree_path(self.mds_path)
        # if hasattr(self.acq, '%s_path' %self.mds_path_components['tree']):
        #     self.tree = MDSplus.Tree(self.mds_path_components['tree'],
        #                                 self.shot)
        #     self.fetch_mode = 'local_path_mode'  # this refers to access by _path e.g. h1data_path
        #                                  # bdb wants to call it local_path_mode, but maybe
        #                                  # TestNoSQLTestDeviceGetdata fails

        # elif self.acq.server_mode == 'mds':
        #     self.acq.connection.openTree(self.mds_path_components['tree'],
        #                                     self.shot)
        #     self.fetch_mode = 'thin client'
        # elif self.acq.server_mode == 'http':
        #     self.fetch_mode = 'http'
        # else:
        #     debug_(DEBUG, level=1, key='Cannot_determine_MDSPlus_fetch_mode')
        #     raise Exception('Cannot determine MDSPlus fetch mode')

    def do_fetch(self):
        print('BBBBBB')
        print(self.pointname)
        print(self.shot)
        
        tmp = self.acq.connection.get('ptdata2("{}",{})'.format(self.pointname, self.shot))
        data = tmp.data()
        print(data)
        tmp = self.acq.connection.get('dim_of(ptdata2("{}",{}))'.format(self.pointname, self.shot))
        t_axis = tmp.data()
        print(t_axis)

        coords = get_coords_for_channel(**self.__dict__)
        ch = Channel(self.pointname, coords)
        # con=MDS.Connection('atlas.gat.com::')
        # pointname = 'MPI66M067D'
        # shot = 164950
        # tmp = con.get('ptdata2("{}",{})'.format(pointname, shot))
        # dat = tmp.data()
        # tmp = con.get('dim_of(ptdata2("{}",{}))'.format(pointname, shot))
        # t = tmp.data()

        output_data = TimeseriesData(timebase=Timebase(t_axis),
                                signal=Signal(data), channels=ch)
        print('BBBBBB2')
        # output_data = super(DIIIDDataFetcherPTdata, self).do_fetch()
        # coords = get_coords_for_channel(**self.__dict__)
        # ch = Channel(self.mds_path, coords)
        # output_data.channels = ch
        # output_data.meta.update({'shot':self.shot, 'kh':self.get_kh()})
        # print(ch)
        output_data.config_name = ch
        self.fetch_mode = 'ptdata'
        return output_data
