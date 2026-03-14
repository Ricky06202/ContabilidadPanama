import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const CTA = () => {
	return (
		<section 
			sx={{ 
				py: { xs: 8, md: 10 }, 
				background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)' 
			}}
		>
			<Container maxWidth="lg">
				<Box textAlign="center">
					<Typography 
						variant="h3" 
						component="h2"
						sx={{ 
							fontWeight: 700, 
							fontSize: { xs: '1.75rem', md: '2.25rem' },
							mb: 2 
						}}
					>
						¿Listo para transformar tu contabilidad?
					</Typography>
					<Typography 
						variant="h6" 
						sx={{ 
							color: 'text.secondary', 
							maxWidth: '500px', 
							mx: 'auto',
							mb: 4 
						}}
					>
						Únete a los contadores y empresarios panameños que ya están usando la herramienta del futuro.
					</Typography>
					<Button
						variant="contained"
						size="large"
						startIcon={<RocketLaunchIcon />}
						sx={{
							background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
							px: 5,
							py: 1.5,
							fontSize: '1.2rem',
							fontWeight: 600,
							borderRadius: '12px',
							textTransform: 'none',
							'&:hover': {
								background: 'linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%)',
							},
						}}
					>
						Comenzar ahora - Es gratis
					</Button>
				</Box>
			</Container>
		</section>
	);
};

export default CTA;