import os
from pyspark.sql import DataFrame
from paramiko import SFTPClient, SSHClient, AutoAddPolicy
from p360_export.export.sfmc.SFMCData import SFMCData


class SFTPUploader:
    def __init__(self, sfmc_data: SFMCData):
        self.__sfmc_data = sfmc_data

    def __get_csv_path(self, export_id: str) -> str:
        return f"/dbfs/tmp/{export_id}.csv"

    def __get_connection(self) -> SFTPClient:
        host = f"{self.__sfmc_data.tenant_url}.ftp.marketingcloudops.com"
        username = self.__sfmc_data.ftp_username
        password = self.__sfmc_data.ftp_password

        ssh = SSHClient()

        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(host, username=username, password=password)

        return ssh.open_sftp()

    def upload(self, df: DataFrame):
        connection = self.__get_connection()

        csv_path = self.__get_csv_path(self.__sfmc_data.export_id)

        df.toPandas().to_csv(csv_path)  # pyre-ignore[16]

        connection.put(csv_path, f"{self.__sfmc_data.ftp_relative_path}{self.__sfmc_data.export_id}.csv")
        connection.close()

        os.remove(csv_path)
