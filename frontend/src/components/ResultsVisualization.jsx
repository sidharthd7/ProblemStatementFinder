import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Container,
  Paper,
  Typography,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert
} from '@mui/material';

const ResultsVisualization = () => {
  const [categoryStats, setCategoryStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [matchingStats, setMatchingStats] = useState({
    totalProblems: 0,
    matchedProblems: 0,
    averageMatchScore: 0,
    topSkills: []
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const [categoryResponse, matchingResponse] = await Promise.all([
          axios.get('/api/analytics/categories'),
          axios.get('/api/analytics/matching-stats')
        ]);
        setCategoryStats(categoryResponse.data);
        setMatchingStats(matchingResponse.data);
        setError(null);
      } catch (error) {
        console.error('Error fetching statistics:', error);
        setError('Failed to load statistics. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Matching Results Overview
        </Typography>

        <Grid container spacing={3} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Total Problems
                </Typography>
                <Typography variant="h3" color="primary">
                  {matchingStats.totalProblems}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Matched Problems
                </Typography>
                <Typography variant="h3" color="primary">
                  {matchingStats.matchedProblems}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Average Match Score
                </Typography>
                <Typography variant="h3" color="primary">
                  {matchingStats.averageMatchScore}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {categoryStats && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Category Distribution
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(categoryStats).map(([category, count], index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">{category}</Typography>
                      <Typography variant="body1" color="text.secondary">
                        {count} problems
                      </Typography>
                      <Box
                        sx={{
                          height: 10,
                          bgcolor: 'primary.light',
                          borderRadius: 1,
                          mt: 1,
                          width: `${(count / matchingStats.totalProblems) * 100}%`
                        }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}

        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Top Required Skills
          </Typography>
          <Grid container spacing={2}>
            {matchingStats.topSkills.map((skill, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{skill.skill}</Typography>
                    <Typography variant="body1" color="text.secondary">
                      Required in {skill.count} problems
                    </Typography>
                    <Box
                      sx={{
                        height: 10,
                        bgcolor: 'primary.light',
                        borderRadius: 1,
                        mt: 1,
                        width: `${(skill.count / matchingStats.totalProblems) * 100}%`
                      }}
                    />
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Paper>
    </Container>
  );
};

export default ResultsVisualization; 