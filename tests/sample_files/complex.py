"""
Complex Python file for testing advanced obfuscation.
"""

import os
import sys
import json
import base64
from datetime import datetime
from collections import defaultdict

class DataProcessor:
    """A class for processing and managing data."""
    
    def __init__(self, config_file=None):
        """Initialize the data processor."""
        self.data_store = defaultdict(list)
        self.config = self._load_config(config_file)
        self.processed_count = 0
        self.error_log = []
    
    def _load_config(self, config_file):
        """Load configuration from file."""
        default_config = {
            "max_items": 1000,
            "output_format": "json",
            "enable_compression": True,
            "log_level": "INFO"
        }
        
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                self.error_log.append(f"Config load error: {e}")
        
        return default_config
    
    def process_item(self, item_data):
        """Process a single data item."""
        try:
            if not isinstance(item_data, dict):
                raise ValueError("Item must be a dictionary")
            
            # Add timestamp
            item_data['processed_at'] = datetime.now().isoformat()
            
            # Add unique ID
            item_data['id'] = f"item_{self.processed_count}"
            
            # Validate required fields
            required_fields = ['name', 'value']
            for field in required_fields:
                if field not in item_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Process based on value type
            if isinstance(item_data['value'], (int, float)):
                item_data['processed_value'] = item_data['value'] * 2
            elif isinstance(item_data['value'], str):
                item_data['processed_value'] = item_data['value'].upper()
            else:
                item_data['processed_value'] = str(item_data['value'])
            
            # Store in appropriate category
            category = item_data.get('category', 'default')
            self.data_store[category].append(item_data)
            
            self.processed_count += 1
            return True
            
        except Exception as e:
            error_msg = f"Processing error for item {self.processed_count}: {e}"
            self.error_log.append(error_msg)
            return False
    
    def process_batch(self, items):
        """Process a batch of items."""
        results = {
            'success': 0,
            'failed': 0,
            'total': len(items)
        }
        
        for item in items:
            if self.process_item(item):
                results['success'] += 1
            else:
                results['failed'] += 1
            
            # Check max items limit
            if self.processed_count >= self.config['max_items']:
                break
        
        return results
    
    def get_statistics(self):
        """Get processing statistics."""
        stats = {
            'total_processed': self.processed_count,
            'categories': {cat: len(items) for cat, items in self.data_store.items()},
            'errors': len(self.error_log),
            'config': self.config
        }
        return stats
    
    def export_data(self, output_file, category=None):
        """Export processed data to file."""
        try:
            if category:
                data_to_export = {category: self.data_store[category]}
            else:
                data_to_export = dict(self.data_store)
            
            output_format = self.config['output_format']
            
            if output_format == 'json':
                with open(output_file, 'w') as f:
                    json.dump(data_to_export, f, indent=2)
            
            elif output_format == 'base64':
                json_str = json.dumps(data_to_export)
                encoded_data = base64.b64encode(json_str.encode()).decode()
                with open(output_file, 'w') as f:
                    f.write(encoded_data)
            
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            return True
            
        except Exception as e:
            self.error_log.append(f"Export error: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources."""
        self.data_store.clear()
        self.processed_count = 0
        if self.error_log:
            print(f"Processing completed with {len(self.error_log)} errors")

def create_sample_data(count=50):
    """Create sample data for testing."""
    sample_items = []
    
    categories = ['electronics', 'books', 'clothing', 'food']
    
    for i in range(count):
        item = {
            'name': f'Item_{i}',
            'value': i * 10 if i % 2 == 0 else f'String_Value_{i}',
            'category': categories[i % len(categories)],
            'metadata': {
                'created_by': 'sample_generator',
                'priority': 'normal' if i % 3 == 0 else 'high'
            }
        }
        sample_items.append(item)
    
    return sample_items

def run_processing_pipeline():
    """Run the complete data processing pipeline."""
    print("Starting data processing pipeline...")
    
    # Initialize processor
    processor = DataProcessor()
    
    # Create sample data
    sample_data = create_sample_data(100)
    print(f"Created {len(sample_data)} sample items")
    
    # Process in batches
    batch_size = 25
    total_results = {'success': 0, 'failed': 0, 'total': 0}
    
    for i in range(0, len(sample_data), batch_size):
        batch = sample_data[i:i + batch_size]
        results = processor.process_batch(batch)
        
        for key in total_results:
            total_results[key] += results[key]
        
        print(f"Batch {i//batch_size + 1}: {results}")
    
    # Get final statistics
    stats = processor.get_statistics()
    print(f"\nFinal statistics: {stats}")
    
    # Export results
    output_file = "processed_data.json"
    if processor.export_data(output_file):
        print(f"Data exported to {output_file}")
    else:
        print("Export failed")
    
    # Cleanup
    processor.cleanup()
    
    return total_results

def main():
    """Main function."""
    try:
        results = run_processing_pipeline()
        
        print("\n" + "="*50)
        print("PROCESSING COMPLETE")
        print("="*50)
        print(f"Total items processed: {results['total']}")
        print(f"Successful: {results['success']}")
        print(f"Failed: {results['failed']}")
        
        success_rate = (results['success'] / results['total']) * 100 if results['total'] > 0 else 0
        print(f"Success rate: {success_rate:.2f}%")
        
    except Exception as e:
        print(f"Pipeline error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
