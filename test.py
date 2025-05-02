import pandas as pd

# Create sample data
data = {
    'Problem Statement': [
        "Create a real-time data analytics dashboard that processes and visualizes IoT sensor data from manufacturing equipment. The system should identify patterns and potential equipment failures.",
        "Develop a natural language processing system to analyze customer feedback and support tickets, categorizing issues and suggesting automated responses.",
        "Build a computer vision system for quality control in a production line, detecting defects in manufactured products using deep learning.",
        "Implement a recommendation engine for an e-commerce platform that suggests products based on user behavior and purchase history.",
        "Create a blockchain-based supply chain tracking system for pharmaceutical products, ensuring authenticity and proper handling conditions."
    ],
    'Technical Requirements': [
        "Python, React, Node.js, MongoDB, Kafka, Docker",
        "Python, NLTK, TensorFlow, FastAPI, PostgreSQL",
        "Python, OpenCV, PyTorch, TensorFlow, Docker, AWS",
        "Python, Spark, Neo4j, FastAPI, React, Redis",
        "Solidity, Node.js, React, MongoDB, AWS"
    ],
    'Complexity Level': [
        "High",
        "Medium",
        "High",
        "Medium",
        "High"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('sample_problems.xlsx', index=False)