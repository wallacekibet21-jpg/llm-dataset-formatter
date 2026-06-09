import json
import os

def run_dataset_pipeline(input_file, output_file):
    print(f"Initializing pipeline execution... Ingesting raw logs from '{input_file}'")
    
    if not os.path.exists(input_file):
        print(f"Error: Target data file '{input_file}' not found.")
        return

    # Ingest the substantial JSON evaluation records
    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    formatted_records = []
    
    # Process and transform individual annotation records into standard LLM schemas
    for record in raw_data:
        if record.get("status") == "approved":
            chat_entry = {
                "messages": [
                    {"role": "user", "content": record["user_prompt"]},
                    {"role": "assistant", "content": record["preferred_model_response"]}
                ]
            }
            formatted_records.append(chat_entry)

    # Save output to industry-standard JSON Lines (.jsonl) file for training ingestion
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in formatted_records:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    print(f"Pipeline successfully converted {len(formatted_records)} evaluation rows.")
    print(f"Output generated successfully at: '{output_file}'")

if __name__ == "__main__":
    # Define source raw logs and target output destination files
    run_dataset_pipeline("raw_evaluations.json", "fine_tuning_dataset.jsonl")
