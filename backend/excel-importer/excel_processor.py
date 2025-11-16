import pandas as pd
import os

class ExcelProcessor:
    def __init__(self):
        self.data_dir = "data/excel-samples"
        self.required_columns = ['sixerclass_id', 'student_name', 'batch_number', 
                                'batch_start_date', 'batch_end_date']
    
    def validate_excel_structure(self, file_path):
        """Validate that Excel file has required columns"""
        
        try:
            df = pd.read_excel(file_path)
            print(f"📊 Excel file loaded: {len(df)} rows")
            print(f"📋 Columns found: {list(df.columns)}")
            
            missing_columns = []
            for col in self.required_columns:
                if col not in df.columns:
                    missing_columns.append(col)
            
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                return False
            
            # Validate data types and content
            validation_errors = []
            
            for index, row in df.iterrows():
                # Check for empty values
                for col in self.required_columns:
                    if pd.isna(row[col]) or str(row[col]).strip() == '':
                        validation_errors.append(f"Row {index+1}: Empty {col}")
                
                # Validate SixerClass ID format
                if not str(row['sixerclass_id']).startswith('SIX'):
                    validation_errors.append(f"Row {index+1}: Invalid SixerClass ID format")
            
            if validation_errors:
                print("❌ Validation errors found:")
                for error in validation_errors[:5]:  # Show first 5 errors
                    print(f"   - {error}")
                if len(validation_errors) > 5:
                    print(f"   ... and {len(validation_errors) - 5} more errors")
                return False
            
            print("✅ Excel file validation passed!")
            return True
            
        except Exception as e:
            print(f"❌ Error validating Excel file: {e}")
            return False
    
    def load_student_data(self, file_path):
        """Load and return student data from Excel"""
        
        try:
            df = pd.read_excel(file_path)
            
            # Convert dates to proper format
            df['batch_start_date'] = pd.to_datetime(df['batch_start_date'])
            df['batch_end_date'] = pd.to_datetime(df['batch_end_date'])
            
            # Fill any missing optional fields
            if 'certificate_generated' not in df.columns:
                df['certificate_generated'] = False
            
            print(f"✅ Loaded {len(df)} students from Excel")
            return df
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return None
    
    def create_sample_excel(self):
        """Create a sample Excel file for testing"""
        
        sample_data = [
            {
                'sixerclass_id': 'SIX001',
                'student_name': 'Rahul Sharma',
                'batch_number': 'AWS-2024-001',
                'batch_start_date': '2024-01-15',
                'batch_end_date': '2024-04-15'
            },
            {
                'sixerclass_id': 'SIX002',
                'student_name': 'Priya Patel',
                'batch_number': 'AWS-2024-001',
                'batch_start_date': '2024-01-15',
                'batch_end_date': '2024-04-15'
            },
            {
                'sixerclass_id': 'SIX003',
                'student_name': 'Amit Kumar',
                'batch_number': 'AWS-2024-002',
                'batch_start_date': '2024-02-01',
                'batch_end_date': '2024-05-01'
            }
        ]
        
        df = pd.DataFrame(sample_data)
        
        # Save to Excel
        output_path = os.path.join(self.data_dir, "student-data.xlsx")
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"✅ Sample Excel file created: {output_path}")
        return output_path

# Test the processor
if __name__ == "__main__":
    processor = ExcelProcessor()
    
    # Create sample Excel if it doesn't exist
    excel_path = os.path.join(processor.data_dir, "student-data.xlsx")
    if not os.path.exists(excel_path):
        processor.create_sample_excel()
    
    # Validate and load
    if processor.validate_excel_structure(excel_path):
        df = processor.load_student_data(excel_path)
        if df is not None:
            print("\n📋 Sample of loaded data:")
            print(df.head())
