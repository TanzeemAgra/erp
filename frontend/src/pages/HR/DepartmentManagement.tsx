import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Add, Business } from '@mui/icons-material';

const DepartmentManagement: React.FC = () => {
  const departments = ['Information Technology', 'Human Resources', 'Finance', 'Operations', 'Sales & Marketing'];
  
  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" fontWeight="bold">
          Department Management
        </Typography>
        <Button variant="contained" startIcon={<Add />} sx={{ borderRadius: 2 }}>
          Add Department
        </Button>
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
        {departments.map((dept) => (
          <Card key={dept}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Business color="primary" sx={{ mr: 2 }} />
                <Typography variant="h6" fontWeight="bold">
                  {dept}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Department for managing {dept.toLowerCase()} operations
              </Typography>
              <Typography variant="h4" color="primary" fontWeight="bold">
                {Math.floor(Math.random() * 20) + 5}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Employees
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default DepartmentManagement;
