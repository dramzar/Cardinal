''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2023 Cardinal Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import MySQLdb
from cardinal.system.common import CardinalEnv


class AccessPoint(CardinalEnv):
    '''
    Object that defines a Cisco access point under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for AccessPoint()
        object
        '''
        super().__init__()

    def add(self, name, ip, subnetMask, sshPort, username, password, community, groupId=None):
        '''
        Method for adding a Cisco access point to Cardinal.
        '''
        conn = self.sql()

        # Encrypt SSH password and SNMP community
        encryptedSshPassword = self.encryption(input=password, action="encrypt")
        encryptedSnmpCommunity = self.encryption(input=community, action="encrypt")

        # Insert access point into the MySQL backend
        try:
            if groupId is None:
                addApCursor = conn.cursor()
                addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_subnetmask, ap_ssh_port, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)",
                (name, ip, subnetMask, sshPort, username, encryptedSshPassword, encryptedSnmpCommunity))
                addApCursor.close()
            else:
                addApCursor = conn.cursor()
                addApCursor.execute("INSERT INTO access_points (ap_name, ap_ip, ap_subnetmask, ap_ssh_port, ap_ssh_username, ap_ssh_password, ap_snmp, ap_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, ip, subnetMask, sshPort, username, encryptedSshPassword, encryptedSnmpCommunity, groupId))
                addApCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def modify(self, id, **kwargs):
        '''
        Method for modifying an existing access point.
        '''
        conn = self.sql()

        # Identify elements of an access point to update via kwargs keys
        if "groupId" in kwargs:
            try:
                updateGroupIdCursor = conn.cursor()
                if kwargs.get("groupId") is not None:
                    updateGroupIdCursor.execute("UPDATE access_points SET ap_group_id = %s WHERE ap_id = %s", (kwargs["groupId"], id))
                else:
                    updateGroupIdCursor.execute("UPDATE access_points SET ap_group_id = NULL WHERE ap_id = %s", [id])
                updateGroupIdCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "ip" in kwargs:
            try:
                updateApIpCursor = conn.cursor()
                updateApIpCursor.execute("UPDATE access_points SET ap_ip = %s WHERE ap_id = %s", (kwargs["ip"], id))
                updateApIpCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "subnetMask" in kwargs:
            try:
                updateApIpCursor = conn.cursor()
                updateApIpCursor.execute("UPDATE access_points SET ap_subnetmask = %s WHERE ap_id = %s", (kwargs["subnetMask"], id))
                updateApIpCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "sshPort" in kwargs:
            try:
                updateApIpCursor = conn.cursor()
                updateApIpCursor.execute("UPDATE access_points SET ap_ssh_port = %s WHERE ap_id = %s", (kwargs["sshPort"], id))
                updateApIpCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "username" in kwargs:
            try:
                updateApSshUserCursor = conn.cursor()
                updateApSshUserCursor.execute("UPDATE access_points SET ap_ssh_username = %s WHERE ap_id = %s", (kwargs["username"], id))
                updateApSshUserCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "name" in kwargs:
            try:
                updateApSshUserCursor = conn.cursor()
                updateApSshUserCursor.execute("UPDATE access_points SET ap_name = %s WHERE ap_id = %s", (kwargs["name"], id))
                updateApSshUserCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "password" in kwargs:

            encryptedSshPassword = self.encryption(input=kwargs["password"], action="encrypt")

            try:
                updateApSshPassCursor = conn.cursor()
                updateApSshPassCursor.execute("UPDATE access_points SET ap_ssh_password = %s WHERE ap_id = %s", (encryptedSshPassword, id))
                updateApSshPassCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

        if "community" in kwargs:

            encryptedSnmpCommunity = self.encryption(input=kwargs["community"], action="encrypt")

            try:
                updateApSnmpCursor = conn.cursor()
                updateApSnmpCursor.execute("UPDATE access_points SET ap_snmp = %s WHERE ap_id = %s", (encryptedSnmpCommunity, id))
                updateApSnmpCursor.close()
            except Exception as e:
                return "ERROR: {}".format(e)
            else:
                conn.commit()

    def delete(self, id=None, **kwargs):
        '''
        Delete an access point from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteApCursor = conn.cursor()
            if 'name' in kwargs:
                deleteApCursor.execute("DELETE FROM access_points WHERE ap_name = %s", [kwargs["name"]])
            else:
                deleteApCursor.execute("DELETE FROM access_points WHERE ap_id = %s", [id])

            deleteApCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)
        except MySQLdb.Error as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, secrets=False, **kwargs):
        '''
        Based on apId provided, grab connection information from MySQL as a tuple
        and return a JSON object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            apInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                if not secrets:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points")
                    apInfo = apInfoCursor.fetchall()
                else:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_ssh_password,ap_snmp,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points")
                    apInfo = apInfoCursor.fetchall()
            else:
                if not secrets:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points WHERE ap_id = %s", [id])
                    apInfo = apInfoCursor.fetchall()
                else:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_ssh_password,ap_snmp,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points WHERE ap_id = %s", [id])
                    apInfo = apInfoCursor.fetchall()

            if "name" in kwargs:
                if not secrets:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points WHERE ap_name = %s", [kwargs["name"]])
                    apInfo = apInfoCursor.fetchall()
                else:
                    apInfoCursor.execute("SELECT ap_id,ap_group_id,ap_name,ap_ip,ap_subnetmask,ap_ssh_port,ap_ssh_username,ap_ssh_password,ap_snmp,ap_total_clients,ap_bandwidth,ap_mac_addr,ap_model,ap_serial,\
                    ap_location,ap_ios_info,ap_uptime FROM access_points WHERE ap_name = %s", [kwargs["name"]])
                    apInfo = apInfoCursor.fetchall()

            apInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            return list(apInfo)

    def changeIp(self, id, newIp, subnetMask):
        '''
        Change access point IP via scout
        '''
        # Get connection information for access point
        changeApIp = self.info(id=id, secrets=True)

        # Invoke scout to execute change IP operation
        sys.scoutChangeIp(ip=changeApIp[0]["ap_ip"], username=changeApIp[0]["ap_ssh_username"], \
        password=self.encryption(input=changeApIp[0]["ap_ssh_password"], action="decrypt"), newIp=newIp, subnetMask=subnetMask)

        # Commit changes to MariaDB backend
        self.modify(id=id, ip=newIp, subnetMask=subnetMask)

    def changeHostname(self, id, hostname):
        '''
        Change access point IP via scout
        '''
        # Get connection information for access point
        changeApHostname = self.info(id=id, secrets=True)

        # Invoke scout to execute change IP operation
        sys.scoutChangeName(ip=changeApHostname[0]["ap_ip"], username=changeApHostname[0]["ap_ssh_username"], \
        password=self.encryption(input=changeApHostname[0]["ap_ssh_password"], action="decrypt"), apName=hostname)

        # Commit changes to MariaDB backend
        self.modify(id=id, name=hostname)

    def tftpBackup(self, id, tftpIp):
        '''
        Change access point IP via scout
        '''
        # Get connection information for access point
        tftpInfo = self.info(id=id, secrets=True)

        # Invoke scout to execute change IP operation
        sys.scoutTftpBackup(ip=tftpInfo[0]["ap_ip"], username=tftpInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=tftpInfo[0]["ap_ssh_password"], action="decrypt"), tftpIp=tftpIp)

    def manageHttp(self, id, status):
        '''
        Manage HTTP service on Cisco AP
        '''
        # Get connection information for access point
        httpInfo = self.info(id=id, secrets=True)

        if status == "enable":
            # Invoke scout to execute enable HTTP operation
            sys.scoutEnableHttp(ip=httpInfo[0]["ap_ip"], username=httpInfo[0]["ap_ssh_username"], \
            password=self.encryption(input=httpInfo[0]["ap_ssh_password"], action="decrypt"))
        elif status == "disable":
            # Invoke scout to execute disable HTTP operation
            sys.scoutDisableHttp(ip=httpInfo[0]["ap_ip"], username=httpInfo[0]["ap_ssh_username"], \
            password=self.encryption(input=httpInfo[0]["ap_ssh_password"], action="decrypt"))
        else:
            return "ERROR: Please select either enable or disable for HTTP operation status."

    def manageSnmp(self, id, status):
        '''
        Manage SNMP service on Cisco AP
        '''
        # Get connection information for access point
        snmpInfo = self.info(id=id, secrets=True)

        if status == "enable":
            # Invoke scout to execute enable SNMP operation
            sys.scoutEnableSnmp(ip=snmpInfo[0]["ap_ip"], username=snmpInfo[0]["ap_ssh_username"], \
            password=self.encryption(input=snmpInfo[0]["ap_ssh_password"], action="decrypt"), snmp=self.encryption(input=snmpInfo[0]["ap_snmp"], action="decrypt"))
        elif status == "disable":
            # Invoke scout to execute disable SNMP operation
            sys.scoutDisableSnmp(ip=snmpInfo[0]["ap_ip"], username=snmpInfo[0]["ap_ssh_username"], \
            password=self.encryption(input=snmpInfo[0]["ap_ssh_password"], action="decrypt"))
        else:
            return "ERROR: Please select either enable or disable for SNMP operation status."

    def deploy24GhzSsid(self, id, ssidId):
        '''
        Deploy 2.4GHz SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid24Ghz().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutCreateSsid24(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        wpa2Pass=self.encryption(input=ssidInfo[0]["ap_ssid_wpa2"], action="decrypt"), vlan=ssidInfo[0]["ap_ssid_vlan"], \
        bridgeGroup=ssidInfo[0]["ap_ssid_bridge_id"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def deploy5GhzSsid(self, id, ssidId):
        '''
        Deploy 5GHz SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid5Ghz().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutCreateSsid5(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        wpa2Pass=self.encryption(input=ssidInfo[0]["ap_ssid_wpa2"], action="decrypt"), vlan=ssidInfo[0]["ap_ssid_vlan"], \
        bridgeGroup=ssidInfo[0]["ap_ssid_bridge_id"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def deploy24GhzRadiusSsid(self, id, ssidId):
        '''
        Deploy 2.4GHz 802.1x SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid24GhzRadius().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutCreateSsid24Radius(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], bridgeGroup=ssidInfo[0]["ap_ssid_bridge_id"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], \
        gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"], radiusIp=ssidInfo[0]["ap_ssid_radius_ip"], sharedSecret=self.encryption(input=apInfo[0]["ap_ssid_radius_secret"], action="decrypt"), \
        authPort=ssidInfo[0]["ap_ssid_authorization_port"], acctPort=ssidInfo[0]["ap_ssid_accounting_port"], radiusTimeout=ssidInfo[0]["ap_ssid_radius_timeout"], \
        radiusGroup=ssidInfo[0]["ap_ssid_radius_group"], methodList=ssidInfo[0]["ap_ssid_radius_method_list"])

    def deploy5GhzRadiusSsid(self, id, ssidId):
        '''
        Deploy 5GHz 802.1x SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid5GhzRadius().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutCreateSsid5Radius(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], bridgeGroup=ssidInfo[0]["ap_ssid_bridge_id"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], \
        gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"], radiusIp=ssidInfo[0]["ap_ssid_radius_ip"], sharedSecret=self.encryption(input=apInfo[0]["ap_ssid_radius_secret"], action="decrypt"), \
        authPort=ssidInfo[0]["ap_ssid_authorization_port"], acctPort=ssidInfo[0]["ap_ssid_accounting_port"], radiusTimeout=ssidInfo[0]["ap_ssid_radius_timeout"], \
        radiusGroup=ssidInfo[0]["ap_ssid_radius_group"], methodList=ssidInfo[0]["ap_ssid_radius_method_list"])


    def remove24GhzSsid(self, id, ssidId):
        '''
        Remove 2.4GHz SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid24Ghz().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutDeleteSsid24(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def remove5GhzSsid(self, id, ssidId):
        '''
        Remove 5GHz SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid5Ghz().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutDeleteSsid5(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def remove24GhzRadiusSsid(self, id, ssidId):
        '''
        Remove 2.4GHz 802.1x SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid24GhzRadius().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutDeleteSsid24(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def remove5GhzRadiusSsid(self, id, ssidId):
        '''
        Remove 5GHz 802.1x SSID to Cisco AP
        '''
        # Get connection information for access point
        apInfo = self.info(id=id, secrets=True)

        # Get SSID deployment information
        ssidInfo = Ssid5GhzRadius().info(id=ssidId, secrets=True)

        # Invoke scout to execute enable HTTP operation
        ssid.scoutDeleteSsid5(ip=apInfo[0]["ap_ip"], username=apInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=apInfo[0]["ap_ssh_password"], action="decrypt"), ssid=ssidInfo[0]["ap_ssid_name"], \
        vlan=ssidInfo[0]["ap_ssid_vlan"], radioSub=ssidInfo[0]["ap_ssid_radio_id"], gigaSub=ssidInfo[0]["ap_ssid_ethernet_id"])

    def fetchInfo(self, id):
        '''
        Change access point IP via scout
        '''
        conn = self.sql()

        # Get connection information for access point
        fetchInfo = self.info(id=id, secrets=True)

        # Invoke scout to execute change IP operation
        apInfo = info.fetcher(ip=fetchInfo[0]["ap_ip"], username=fetchInfo[0]["ap_ssh_username"], \
        password=self.encryption(input=fetchInfo[0]["ap_ssh_password"], action="decrypt"))

        # Commit changes to MariaDB backend
        apMacAddr = apInfo[0]
        apBandwidth = apInfo[1].strip("Mbps")
        apIosInfo = apInfo[2]
        apUptime = apInfo[3]
        apSerial = apInfo[4]
        apModel = apInfo[5]
        apClientCount = apInfo[6]
        apLocation = apInfo[7]
        apInfoCursor = conn.cursor()
        apInfoCursor.execute("UPDATE access_points SET ap_bandwidth = %s, ap_mac_addr = %s, ap_model = %s, ap_serial = %s, ap_location = %s,"
        "ap_ios_info = %s, ap_uptime = %s, ap_total_clients = %s WHERE ap_id = %s", (apBandwidth,apMacAddr,apModel,apSerial,
        apLocation,apIosInfo,apUptime,apClientCount,id))
        conn.commit()
        apInfoCursor.close()

        return apInfo

class AccessPointGroup(CardinalEnv):
    '''
    Object that defines an access point group under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for AccessPointGroup() object.
        '''
        super().__init__()

    def add(self, name):
        '''
        Method for adding a Cisco access point group to Cardinal.
        '''
        conn = self.sql()

        # Insert access point group into the MySQL backend
        try:
            addApGroupCursor = conn.cursor()
            addApGroupCursor.execute("INSERT INTO access_point_groups (ap_group_name) VALUES (%s)", [name])
            addApGroupCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def modify(self, id, **kwargs):
        '''
        Method for modifying an existing access point group's name.
        '''
        conn = self.sql()

        try:
            updateApGroupCursor = conn.cursor()
            updateApGroupCursor.execute("UPDATE access_point_groups SET ap_group_name = %s WHERE ap_group_id = %s", (kwargs["name"], id))
            updateApGroupCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id=None, **kwargs):
        '''
        Delete an access point group from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteApGroupCursor = conn.cursor()
            if 'name' in kwargs:
                deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_name = %s", [kwargs["name"]])
            else:
                deleteApGroupCursor.execute("DELETE FROM access_point_groups WHERE ap_group_id = %s", [id])

            deleteApGroupCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def iterator(self, id, snmp="False", **kwargs):
        '''
        Used to create a list of lists, which is then passed
        into functions such as processor().
        '''
        conn = self.sql()

        # Handle SNMP logic
        try:
            apInfoCursor = conn.cursor()
            if snmp == "True":
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password,ap_snmp FROM access_points WHERE ap_group_id = %s", [id])
            elif snmp == "False":
                apInfoCursor.execute("SELECT ap_ip,ap_ssh_username,ap_ssh_password FROM access_points WHERE ap_group_id = %s", [id])
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            apInfoSql = apInfoCursor.fetchall()
            apInfoCursor.close()

        # Create a list object for incrementing access point data
        apList = []

        for i in apInfoSql:
            connInfo = []
            apIp = connInfo.append(i[0])
            apSshUsername = connInfo.append(i[1])
            apSshPassword = connInfo.append(self.encryption(input=i[2], action="decrypt"))
            if snmp == "True":
                apSnmp = connInfo.append(self.encryption(input=i[3], action="decrypt"))
            addedArgs = list(kwargs.values())
            apInfo = connInfo + addedArgs # Combine the two lists into one named apInfo[].
            apList.append(apInfo)

        return apList

    def processor(self, operation, apInfo):
        '''
        processor() is used for parallel processing. processor()
        accepts two positional arguments: operation and apInfo. operation is
        the function itself (e.g. scout_sys.scoutDoWr) and apInfo is a list of parameters
        that is passed for each access point (e.g. connection information).
        '''
        with multiprocessing.Pool(processes=int(self.tunings['workers'])) as tasker:
            taskResults = tasker.starmap(operation, apInfo)

        return taskResults

    def info(self, id=None, **kwargs):
        '''
        Based on groupId provided, grab connection information from MySQL as a tuple
        and return a JSON object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            apGroupInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                apGroupInfoCursor.execute("SELECT access_point_groups.ap_group_id, access_point_groups.ap_group_name, FORMAT(SUM(access_points.ap_total_clients),0) AS ap_group_total_clients FROM \
                access_point_groups LEFT JOIN access_points ON access_point_groups.ap_group_id=access_points.ap_group_id GROUP BY access_point_groups.ap_group_id, access_point_groups.ap_group_name")
                apGroupInfo = apGroupInfoCursor.fetchall()
            else:
                apGroupInfoCursor.execute("SELECT access_point_groups.ap_group_id, access_point_groups.ap_group_name, FORMAT(SUM(access_points.ap_total_clients),0) AS ap_group_total_clients FROM \
                access_point_groups LEFT JOIN access_points ON access_point_groups.ap_group_id=access_points.ap_group_id WHERE access_point_groups.ap_group_id = %s", [id])
                apGroupInfo = apGroupInfoCursor.fetchall()

            if "name" in kwargs:
                apGroupInfoCursor.execute("SELECT access_point_groups.ap_group_id, access_point_groups.ap_group_name, FORMAT(SUM(access_points.ap_total_clients),0) AS ap_group_total_clients FROM \
                access_point_groups LEFT JOIN access_points ON access_point_groups.ap_group_id=access_points.ap_group_id WHERE access_point_groups.ap_group_name = %s", [kwargs["name"]])
                apGroupInfo = apGroupInfoCursor.fetchall()

            apGroupInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            if "struct" in kwargs:
                if kwargs["struct"] == "dict":
                    apGroupJson = json.dumps(apGroupInfo)
                    return json.loads(apGroupJson)
            return list(apGroupInfo)

class Ssid24Ghz(CardinalEnv):
    '''
    Object that defines a 2.4GHz SSID under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for Ssid() object.
        '''
        super().__init__()

    def add(self, name, vlan, wpa2, bridgeGroup, radioId, gigaId):
        '''
        Method for adding a 2.4GHz SSID to Cardinal.
        '''
        conn = self.sql()

        # Encrypt WPA2 passphrase
        encryptedWpa2 = self.encryption(input=wpa2, action="encrypt")

        try:
            addSsidCursor = conn.cursor()
            addSsidCursor.execute("INSERT INTO ssids_24ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) \
            VALUES (%s, %s, %s, %s, %s, %s)",
            (name, vlan, encryptedWpa2, bridgeGroup, radioId, gigaId))
            addSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a 2.4GHz SSID from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteSsidCursor = conn.cursor()
            deleteSsidCursor.execute("DELETE FROM ssids_24ghz WHERE ap_ssid_id = %s", [id])
            deleteSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, secrets=False, **kwargs):
        '''
        Based on id provided, return SSID information
        as a dict() object. If no id is provided, return all
        SSIDs available.
        '''
        conn = self.sql()

        try:
            ssidInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz")
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz")
                    ssidInfo = ssidInfoCursor.fetchall()
            else:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()

            if "name" in kwargs:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_24ghz WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()

            ssidInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(ssidInfo)

class Ssid5Ghz(CardinalEnv):
    '''
    Object that defines a 5GHz SSID under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for Ssid() object.
        '''
        super().__init__()

    def add(self, name, vlan, wpa2, bridgeGroup, radioId, gigaId):
        '''
        Method for adding a 5GHz SSID to Cardinal.
        '''
        conn = self.sql()

        # Encrypt WPA2 passphrase
        encryptedWpa2 = self.encryption(input=wpa2, action="encrypt")

        try:
            addSsidCursor = conn.cursor()
            addSsidCursor.execute("INSERT INTO ssids_5ghz (ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id) \
            VALUES (%s, %s, %s, %s, %s, %s)",
            (name, vlan, encryptedWpa2, bridgeGroup, radioId, gigaId))
            addSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a 5GHz SSID from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteSsidCursor = conn.cursor()
            deleteSsidCursor.execute("DELETE FROM ssids_5ghz WHERE ap_ssid_id = %s", [id])
            deleteSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, secrets=False, **kwargs):
        '''
        Based on ssidId provided, grab connection information from MySQL as a tuple
        and return a JSON object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            ssidInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz")
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz")
                    ssidInfo = ssidInfoCursor.fetchall()
            else:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()

            if "name" in kwargs:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_wpa2, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id FROM ssids_5ghz WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()

            ssidInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(ssidInfo)

class Ssid24GhzRadius(CardinalEnv):
    '''
    Object that defines a 2.4GHz RADIUS SSID under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for Ssid() object.
        '''
        super().__init__()

    def add(self, name, vlan, bridgeGroup, radioId, gigaId, radiusIp, sharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList):
        '''
        Method for adding a 2.4GHz 802.1x SSID to Cardinal.
        '''
        conn = self.sql()

        # Encrypt sensitive values
        encryptedSharedSecret = self.encryption(input=sharedSecret, action="encrypt")

        try:
            addSsidCursor = conn.cursor()
            addSsidCursor.execute("INSERT INTO ssids_24ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id,\
            ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port,\
            ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (name, vlan, bridgeGroup, radioId, gigaId, radiusIp, encryptedSharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList))
            addSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a 2.4GHz 802.1x SSID from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteSsidCursor = conn.cursor()
            deleteSsidCursor.execute("DELETE FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [id])
            deleteSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, secrets=False, **kwargs):
        '''
        Based on ssidId provided, grab connection information from MySQL as a tuple
        and return a JSON object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            ssidInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius")
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius")
                    ssidInfo = ssidInfoCursor.fetchall()
            else:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()

            if "name" in kwargs:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret,ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_24ghz_radius WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()

            ssidInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(ssidInfo)

class Ssid5GhzRadius(CardinalEnv):
    '''
    Object that defines a 5GHz RADIUS SSID under
    Cardinal management.
    '''
    def __init__(self):
        '''
        Default constructor for Ssid() object.
        '''
        super().__init__()

    def add(self, name, vlan, bridgeGroup, radioId, gigaId, radiusIp, sharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList):
        '''
        Method for adding a 5GHz 802.1x SSID to Cardinal.
        '''
        conn = self.sql()

        # Encrypt sensitive values
        encryptedSharedSecret = self.encryption(input=sharedSecret, action="encrypt")

        try:
            addSsidCursor = conn.cursor()
            addSsidCursor.execute("INSERT INTO ssids_5ghz_radius (ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, \
            ap_ssid_ethernet_id, ap_ssid_radius_server, ap_ssid_radius_secret,ap_ssid_authorization_port, ap_ssid_accounting_port, \
            ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (name, vlan, bridgeGroup, radioId, gigaId, radiusIp, encryptedSharedSecret, authPort, acctPort, radiusTimeout, radiusGroup, methodList))
            addSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a 5GHz 802.1x SSID from Cardinal management.
        '''
        conn = self.sql()

        try:
            deleteSsidCursor = conn.cursor()
            deleteSsidCursor.execute("DELETE FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [id])
            deleteSsidCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, secrets=False, **kwargs):
        '''
        Based on ssidId provided, grab connection information from MySQL as a tuple
        and return a JSON object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            ssidInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
            if id is None:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius")
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius")
                    ssidInfo = ssidInfoCursor.fetchall()
            else:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret, ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius WHERE ap_ssid_id = %s", [id])
                    ssidInfo = ssidInfoCursor.fetchall()

            if "name" in kwargs:
                if not secrets:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()
                else:
                    ssidInfoCursor.execute("SELECT ap_ssid_id, ap_ssid_name, ap_ssid_vlan, ap_ssid_bridge_id, ap_ssid_radio_id, ap_ssid_ethernet_id, ap_ssid_radius_server, \
                    ap_ssid_radius_secret,ap_ssid_authorization_port, ap_ssid_accounting_port, ap_ssid_radius_timeout, ap_ssid_radius_group, ap_ssid_radius_method_list FROM ssids_5ghz_radius WHERE ap_ssid_name = %s", [kwargs["name"]])
                    ssidInfo = ssidInfoCursor.fetchall()

            ssidInfoCursor.close()

        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(ssidInfo)
