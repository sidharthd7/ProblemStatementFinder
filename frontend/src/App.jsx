import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  CssBaseline,
  Box
} from '@mui/material';
import ProblemUpload from './components/ProblemUpload';
import TeamProfile from './components/TeamProfile';
import ProblemMatching from './components/ProblemMatching';
import ResultsVisualization from './components/ResultsVisualization';

function App() {
  return (
    <Router>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Problem Statement Finder
            </Typography>
            <Button color="inherit" component={Link} to="/upload">
              Upload Problem
            </Button>
            <Button color="inherit" component={Link} to="/team">
              Team Profile
            </Button>
            <Button color="inherit" component={Link} to="/matching">
              Problem Matching
            </Button>
            <Button color="inherit" component={Link} to="/results">
              Results
            </Button>
          </Toolbar>
        </AppBar>
      </Box>

      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/upload" element={<ProblemUpload />} />
          <Route path="/team" element={<TeamProfile />} />
          <Route path="/matching" element={<ProblemMatching />} />
          <Route path="/results" element={<ResultsVisualization />} />
          <Route path="/" element={<ProblemMatching />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
