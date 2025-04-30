import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  Container,
  Chip,
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';

const TeamProfile = () => {
  const [teamData, setTeamData] = useState({
    team_size: 0,
    technical_skills: [],
    preferred_domains: [],
    deadline: null
  });

  const [skillInput, setSkillInput] = useState('');
  const [skillLevel, setSkillLevel] = useState('Intermediate');
  const [domainInput, setDomainInput] = useState('');

  const handleAddSkill = () => {
    if (skillInput.trim()) {
      setTeamData({
        ...teamData,
        technical_skills: [...teamData.technical_skills, {
          skill: skillInput.trim(),
          proficiency_level: skillLevel
        }]
      });
      setSkillInput('');
    }
  };

  const handleAddDomain = () => {
    if (domainInput.trim()) {
      setTeamData({
        ...teamData,
        preferred_domains: [...teamData.preferred_domains, domainInput.trim()]
      });
      setDomainInput('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/match-problems', teamData);
      console.log('Team profile submitted successfully:', response.data);
    } catch (error) {
      console.error('Error submitting team profile:', error);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Create Team Profile
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            type="number"
            label="Team Size"
            margin="normal"
            value={teamData.team_size}
            onChange={(e) => setTeamData({ ...teamData, team_size: parseInt(e.target.value) || 0 })}
          />
          
          <TextField
            fullWidth
            type="datetime-local"
            label="Deadline"
            margin="normal"
            InputLabelProps={{ shrink: true }}
            value={teamData.deadline || ''}
            onChange={(e) => setTeamData({ ...teamData, deadline: e.target.value })}
          />
          
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Technical Skills
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <TextField
                label="Add Skill"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
              />
              <FormControl sx={{ minWidth: 120 }}>
                <InputLabel>Level</InputLabel>
                <Select
                  value={skillLevel}
                  label="Level"
                  onChange={(e) => setSkillLevel(e.target.value)}
                >
                  <MenuItem value="Beginner">Beginner</MenuItem>
                  <MenuItem value="Intermediate">Intermediate</MenuItem>
                  <MenuItem value="Expert">Expert</MenuItem>
                </Select>
              </FormControl>
              <Button variant="contained" onClick={handleAddSkill}>
                Add Skill
              </Button>
            </Box>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {teamData.technical_skills.map((skill, index) => (
                <Chip
                  key={index}
                  label={`${skill.skill} (${skill.proficiency_level})`}
                  onDelete={() => {
                    const newSkills = teamData.technical_skills.filter((_, i) => i !== index);
                    setTeamData({ ...teamData, technical_skills: newSkills });
                  }}
                />
              ))}
            </Stack>
          </Box>

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Preferred Domains
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <TextField
                label="Add Domain"
                value={domainInput}
                onChange={(e) => setDomainInput(e.target.value)}
              />
              <Button variant="contained" onClick={handleAddDomain}>
                Add Domain
              </Button>
            </Box>
            <Stack direction="row" spacing={1} flexWrap="wrap">
              {teamData.preferred_domains.map((domain, index) => (
                <Chip
                  key={index}
                  label={domain}
                  onDelete={() => {
                    const newDomains = teamData.preferred_domains.filter((_, i) => i !== index);
                    setTeamData({ ...teamData, preferred_domains: newDomains });
                  }}
                />
              ))}
            </Stack>
          </Box>

          <Button
            type="submit"
            variant="contained"
            color="primary"
            sx={{ mt: 3 }}
          >
            Create Team Profile
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default TeamProfile;
