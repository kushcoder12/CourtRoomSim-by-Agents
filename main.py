#!/usr/bin/env python3
"""
AI Courtroom Simulation

This script runs a simulated courtroom debate between AI agents representing
opposing sides of a legal case about the rights of book authors versus LLM companies.

Usage:
    python main.py --judge_model /path/to/judge/model 
                  --lawyer_for_model /path/to/lawyer/for/model 
                  --lawyer_against_model /path/to/lawyer/against/model 
                  --for_motion_doc /path/to/for/motion/doc 
                  --against_motion_doc /path/to/against/motion/doc 
                  --output /path/to/output.txt
"""

import os
import sys
import argparse
import torch
from app.config import SimulationConfig
from app.models.model_loader import load_model
from app.models.document_indexer import DocumentIndexer
from app.lawyers import LawyerAgent
from app.judge import JudgeAgent
from app.simulation import CourtSimulation

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AI Courtroom Simulation")
    
    parser.add_argument("--judge_model", 
                        help="Path to the judge model")
    parser.add_argument("--lawyer_for_model", 
                        help="Path to the model for counsel arguing for the motion")
    parser.add_argument("--lawyer_against_model", 
                        help="Path to the model for counsel arguing against the motion")
    parser.add_argument("--for_motion_doc", 
                        help="Path to document with arguments for the motion")
    parser.add_argument("--against_motion_doc", 
                        help="Path to document with arguments against the motion")
    parser.add_argument("--output", 
                        help="Path to save the transcript output")
    parser.add_argument("--case_description", 
                        help="Custom case description")
    
    return parser.parse_args()

def main():
    """Main function to run the simulation"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Create configuration
    config = SimulationConfig(
        case_description=args.case_description,
        for_motion_doc=args.for_motion_doc,
        against_motion_doc=args.against_motion_doc,
        transcript_output=args.output,
        judge_model_path=args.judge_model,
        lawyer_for_model_path=args.lawyer_for_model,
        lawyer_against_model_path=args.lawyer_against_model
    )
    
    # Validate configuration
    is_valid, error_message = config.validate()
    if not is_valid:
        print(f"Error: {error_message}")
        print("Please provide valid model and document paths.")
        sys.exit(1)
    
    # Print configuration
    print("\n=== AI Courtroom Simulation ===")
    print(f"Judge model: {config.judge_model_path}")
    print(f"Lawyer 'for' model: {config.lawyer_for_model_path}")
    print(f"Lawyer 'against' model: {config.lawyer_against_model_path}")
    print(f"Document for motion: {config.for_motion_doc}")
    print(f"Document against motion: {config.against_motion_doc}")
    print(f"Output transcript: {config.transcript_output}")
    print("===============================\n")
    
    # Initialize document indexer
    print("Setting up document retrieval system...")
    document_indexer = DocumentIndexer()
    
    # Load and chunk documents
    doc_for_chunks = document_indexer.load_and_chunk_document(config.for_motion_doc)
    doc_against_chunks = document_indexer.load_and_chunk_document(config.against_motion_doc)
    
    # Create vector stores
    vector_store_for = document_indexer.create_faiss_index(doc_for_chunks, "for_motion")
    vector_store_against = document_indexer.create_faiss_index(doc_against_chunks, "against_motion")
    
    # Create combined vector store
    combined_chunks = doc_for_chunks + doc_against_chunks
    combined_vector_store = document_indexer.create_faiss_index(combined_chunks)
    
    print("Document retrieval system ready")
    
    # Load AI models
    print("\nLoading AI models...")
    judge_model, judge_tokenizer = load_model(config.judge_model_path)
    lawyer_for_model, lawyer_for_tokenizer = load_model(config.lawyer_for_model_path)
    lawyer_against_model, lawyer_against_tokenizer = load_model(config.lawyer_against_model_path)
    print("Models loaded successfully")
    
    # Create agents
    judge_agent = JudgeAgent(
        judge_model,
        judge_tokenizer,
        combined_vector_store,
        config.case_description
    )
    
    lawyer_for = LawyerAgent(
        "for",
        lawyer_for_model,
        lawyer_for_tokenizer,
        vector_store_for,
        config.case_description
    )
    
    lawyer_against = LawyerAgent(
        "against",
        lawyer_against_model,
        lawyer_against_tokenizer,
        vector_store_against,
        config.case_description
    )
    
    # Create and run simulation
    print("\nStarting courtroom simulation...\n")
    simulation = CourtSimulation(
        config.case_description,
        judge_agent,
        lawyer_for,
        lawyer_against,
        document_indexer,
        config.transcript_output
    )
    
    # Run the simulation
    simulation.run_simulation()
    
    # Print final message
    print(f"\nSimulation complete. Results saved to {config.transcript_output}")

if __name__ == "__main__":
    main() 