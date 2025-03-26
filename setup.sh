#!/bin/bash
# Setup script for AI Courtroom Simulation

echo "Setting up AI Courtroom Simulation..."

# Ensure the original file is not confusing users
if [ -f "coutrroomsim" ]; then
    echo "Archiving original code file..."
    mkdir -p archive
    mv coutrroomsim archive/
fi

# Create necessary directories
mkdir -p data/inputs models

# Check if the sample documents are already in place
if [ ! -f "data/inputs/for_motion.txt" ] || [ ! -f "data/inputs/against_motion.txt" ]; then
    echo "Sample documents are missing. Please create the following files:"
    echo "- data/inputs/for_motion.txt (arguments supporting book authors)"
    echo "- data/inputs/against_motion.txt (arguments supporting LLM companies)"
fi

# Install dependencies
echo "Installing required Python packages..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run the simulation, you need to provide paths to three language models."
echo "Example command:"
echo ""
echo "python main.py \\"
echo "  --judge_model /path/to/judge/model \\"
echo "  --lawyer_for_model /path/to/lawyer/for/model \\"
echo "  --lawyer_against_model /path/to/lawyer/against/model \\"
echo "  --output courtroom_transcript.txt"
echo ""
echo "For more information, see the README.md file." 