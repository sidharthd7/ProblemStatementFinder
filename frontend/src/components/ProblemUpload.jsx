import React, { useState } from 'react';
import axios from 'axios';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Paper,
  Container,
  Alert,
  Snackbar,
  CircularProgress
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const ProblemUpload = () => {
  const [problemData, setProblemData] = useState({
    title: '',
    description: '',
    requirements: {
      min_team_size: '',
      max_team_size: '',
      required_skills: '',
      estimated_duration_weeks: '',
      difficulty_level: ''
    },
    attachments: null
  });

  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!problemData.attachments?.[0]) {
      setNotification({
        open: true,
        message: 'Please select an Excel file to upload',
        severity: 'error'
      });
      return;
    }

    // Verify file type
    const file = problemData.attachments[0];
    if (!file.name.match(/\.(xlsx|xls)$/)) {
      setNotification({
        open: true,
        message: 'Please upload only Excel files (.xlsx or .xls)',
        severity: 'error'
      });
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      const response = await axios.post('/api/upload-problems', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setNotification({
        open: true,
        message: response.data.message || 'Problem Statement uploaded successfully!',
        severity: 'success'
      });
      // Reset form
      setProblemData({
        title: '',
        description: '',
        requirements: {
          min_team_size: '',
          max_team_size: '',
          required_skills: '',
          estimated_duration_weeks: '',
          difficulty_level: ''
        },
        attachments: null
      });
    } catch (error) {
      setNotification({
        open: true,
        message: error.response?.data?.detail || 'Error uploading problem statement',
        severity: 'error'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Upload Problem Statement
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            required
            label="Problem Title"
            margin="normal"
            value={problemData.title}
            onChange={(e) => setProblemData({ ...problemData, title: e.target.value })}
          />
          <TextField
            fullWidth
            required
            label="Problem Description"
            margin="normal"
            multiline
            rows={4}
            value={problemData.description}
            onChange={(e) => setProblemData({ ...problemData, description: e.target.value })}
          />
          
          <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
            Requirements
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <TextField
              type="number"
              label="Min Team Size"
              value={problemData.requirements.min_team_size}
              onChange={(e) => setProblemData({
                ...problemData,
                requirements: { ...problemData.requirements, min_team_size: e.target.value }
              })}
            />
            <TextField
              type="number"
              label="Max Team Size"
              value={problemData.requirements.max_team_size}
              onChange={(e) => setProblemData({
                ...problemData,
                requirements: { ...problemData.requirements, max_team_size: e.target.value }
              })}
            />
          </Box>

          <TextField
            fullWidth
            label="Required Skills (comma-separated)"
            margin="normal"
            value={problemData.requirements.required_skills}
            onChange={(e) => setProblemData({
              ...problemData,
              requirements: { ...problemData.requirements, required_skills: e.target.value }
            })}
          />

          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <TextField
              type="number"
              label="Estimated Duration (weeks)"
              value={problemData.requirements.estimated_duration_weeks}
              onChange={(e) => setProblemData({
                ...problemData,
                requirements: { ...problemData.requirements, estimated_duration_weeks: e.target.value }
              })}
            />
            <TextField
              label="Difficulty Level"
              value={problemData.requirements.difficulty_level}
              onChange={(e) => setProblemData({
                ...problemData,
                requirements: { ...problemData.requirements, difficulty_level: e.target.value }
              })}
            />
          </Box>

          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUploadIcon />}
            sx={{ mt: 3, mr: 2 }}
          >
            Upload Excel File
            <input
              type="file"
              hidden
              accept=".xlsx,.xls"
              onChange={(e) => setProblemData({ ...problemData, attachments: e.target.files })}
            />
          </Button>
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            sx={{ mt: 3 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Submit Problem Statement'}
          </Button>
        </Box>
      </Paper>

      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
      >
        <Alert
          onClose={handleCloseNotification}
          severity={notification.severity}
          sx={{ width: '100%' }}
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ProblemUpload;

