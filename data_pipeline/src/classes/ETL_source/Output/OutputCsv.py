from data_pipeline.src.classes.ETL_source.Output.Output import Output
import pandas as pd

class OutputCsv(Output):
    def add_data_source(self, data_source):
        self.data_sources.append(data_source)

    def combine_data(self):
        combined_data = pd.DataFrame()
        for source in self.data_sources:
            source.create_path()
            source.check_for_new_files()
            data = source.get_data()
            if data is not None:
                combined_data = pd.concat([combined_data, data], ignore_index=True)
                print(combined_data)
        return combined_data
        
    def save_to_csv(self):
        self.create_folder_path_data_frames(self.output_file_csv)
        combined_data = self.combine_data()
        combined_data.to_csv(self.file_path_csv, index=False)
        print(f"Combined data saved to {self.output_file_csv}")

    def check_and_transforme_csv(self):
    # Combinação dos dados e salvamento em um arquivo CSV
        self.add_data_source(self.csv_source)
        self.add_data_source(self.json_source)
        self.add_data_source(self.txt_source)
        self.save_to_csv()
