import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Stack,
  Card,
  CardContent,
  Button
} from '@mui/material';

const ProblemMatching = () => {
  const [searchParams, setSearchParams] = useState({
    query: '',
    category: 'all',
    tech_stack: [],
    difficulty: null
  });

  const [problems, setProblems] = useState([]);
  const [matchedProblems, setMatchedProblems] = useState([]);

  const handleFilterChange = (field, value) => {
    setSearchParams({
      ...searchParams,
      [field]: value
    });
  };

  const handleSearch = async () => {
    try {
      const response = await axios.get('/api/problems/search', {
        params: searchParams
      });
      setProblems(response.data);
    } catch (error) {
      console.error('Error searching problems:', error);
    }
  };

  const handleMatchProblems = async (teamProfile) => {
    try {
      const response = await axios.post('/api/match-problems', {
        team_profile: teamProfile,
        min_score: 0.5,
        limit: 10
      });
      setMatchedProblems(response.data.matches);
    } catch (error) {
      console.error('Error matching problems:', error);
    }
  };

  return (
    <Container maxWidth="lg">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Problem Matching
        </Typography>
        
        <Box sx={{ mb: 4 }}>
          <TextField
            fullWidth
            label="Search Problems"
            margin="normal"
            value={searchParams.query}
            onChange={(e) => handleFilterChange('query', e.target.value)}
          />
          
          <FormControl fullWidth margin="normal">
            <InputLabel>Category</InputLabel>
            <Select
              value={searchParams.category}
              label="Category"
              onChange={(e) => handleFilterChange('category', e.target.value)}
            >
              <MenuItem value="all">All Categories</MenuItem>
              <MenuItem value="web">Web Development</MenuItem>
              <MenuItem value="mobile">Mobile Development</MenuItem>
              <MenuItem value="ai">AI/ML</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="contained"
            color="primary"
            onClick={handleSearch}
            sx={{ mt: 2 }}
          >
            Search
          </Button>
        </Box>

        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Matched Problems
          </Typography>
          <Stack spacing={2}>
            {problems.map((problem) => (
              <Card key={problem.id}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {problem.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {problem.description}
                  </Typography>
                  <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
                    {problem.requiredSkills.map((skill, index) => (
                      <Chip key={index} label={skill} size="small" />
                    ))}
                  </Stack>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body1" color="primary">
                      Match Score: {problem.matchScore}%
                    </Typography>
                    <Button variant="contained" size="small">
                      View Details
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Stack>
        </Box>
      </Paper>
    </Container>
  );
};

export default ProblemMatching; 