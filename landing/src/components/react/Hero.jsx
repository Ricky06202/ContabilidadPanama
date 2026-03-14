import React from 'react';
import { Button, Container, Typography, Box, useTheme } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

const Hero = () => {
	const theme = useTheme();
	
	return (
		<section 
			style={{
				background: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
				paddingTop: '120px',
				paddingBottom: '80px',
				minHeight: '100vh',
				display: 'flex',
				alignItems: 'center',
				boxSizing: 'border-box',
			}}
		>
			<Container maxWidth="lg">
				<Box 
					display="flex" 
					flexDirection="column" 
					alignItems="center" 
					textAlign="center"
					sx={{ gap: 4 }}
				>
					<Typography 
						variant="h2" 
						component="h1"
						sx={{
							fontWeight: 800,
							fontSize: { xs: '2.5rem', md: '4rem' },
							background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
							WebkitBackgroundClip: 'text',
							WebkitTextFillColor: 'transparent',
							backgroundClip: 'text',
							mb: 2,
						}}
					>
						El futuro de la contabilidad en Panamá
					</Typography>
					<Typography 
						variant="h5" 
						component="p"
						sx={{
							color: 'text.secondary',
							maxWidth: '600px',
							fontSize: { xs: '1.1rem', md: '1.25rem' },
							mb: 2,
						}}
					>
						Plataforma moderna de contabilidad construida para contadores y empresarios panameños. 
						Reemplaza MYOB con una experiencia fluida, rápida y diseñada para el futuro.
					</Typography>
					<Button
							variant="contained"
							size="large"
							startIcon={<PlayArrowIcon />}
							href="https://app.contapanama.rsanjur.com"
							sx={{
								background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
								px: 4,
								py: 1.5,
								fontSize: '1.1rem',
								fontWeight: 600,
								borderRadius: '12px',
								textTransform: 'none',
								'&:hover': {
									background: 'linear-gradient(135deg, #1d4ed8 0%, #6d28d9 100%)',
								},
							}}
						>
							Comenzar ahora
						</Button>
				</Box>
			</Container>
		</section>
	);
};

export default Hero;