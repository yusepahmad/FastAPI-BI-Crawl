from .hardcode import HardCode

class SoftCode(HardCode):
    def __init__(self):
        super().__init__()

    def hehe(self):
        return 'hehe'

    async def kurs_data(self, option, akses, start, end):
        if option == "Time Series":
            file_path = f"s3://ai-pipeline-statistics/API/BI/Nilai Tukar Mata Uang/{akses}/{option}/{start}-{end}.json"
        else:
            file_path = f"s3://ai-pipeline-statistics/API/BI/Nilai Tukar Mata Uang/{akses}/{option}/{start}.json"
        s3_check =  self.check(file_path)
        if s3_check:
            response = s3_check
        else:
            response = await self.kurs(option, akses, start, end)
            self.send_json_s3_v2(response, path_data_raw=file_path, file_name_json=file_path.split('/')[-1])
        return response

    async def data_inflasi(self, start, end):
        file_path = f"s3://ai-pipeline-statistics/API/BI/Data inflasi/{start}-{end}.json"
        s3_check =  self.check(file_path)
        if s3_check:
            response = s3_check
        else:
            response = await self.dana_inflasi(start,  end)
            self.send_json_s3_v2(response, path_data_raw=file_path, file_name_json=file_path.split('/')[-1])
        return response

    async def data_suku_bunga(self, start, end):
        file_path = f"s3://ai-pipeline-statistics/API/BI/Data tingkat suku bunga/{start}-{end}.json"
        s3_check =  self.check(file_path)
        if s3_check:
            response = s3_check
        else:
            response = await self.data_suku(start,  end)
            self.send_json_s3_v2(response, path_data_raw=file_path, file_name_json=file_path.split('/')[-1])
        return response
