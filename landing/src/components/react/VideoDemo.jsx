import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

const VideoDemo = () => {
	return (
		<section sx={{ py: { xs: 12, md: 16 }, backgroundColor: '#1e293b' }}>
			<Container maxWidth="lg">
				<Box textAlign="center" mb={8}>
					<Typography 
						variant="h3" 
						component="h2"
						sx={{ 
							fontWeight: 700, 
							fontSize: { xs: '2rem', md: '2.5rem' },
							mb: 3,
							color: 'white'
						}}
					>
						Ve ContabilidadPanama en acción
					</Typography>
					<Typography variant="h6" sx={{ color: '#94a3b8', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Descubre cómo nuestra plataforma puede transformar tu negocio
					</Typography>
				</Box>

				<Box 
					sx={{
						position: 'relative',
						borderRadius: 4,
						overflow: 'hidden',
						boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
						maxWidth: '900px',
						mx: 'auto',
						aspectRatio: '16/9',
						backgroundColor: '#0f172a',
						display: 'flex',
						alignItems: 'center',
						justifyContent: 'center',
						cursor: 'pointer',
						transition: 'all 0.3s ease',
						'&:hover': {
							transform: 'scale(1.02)',
						},
					}}
				>
					<Box 
						sx={{
							position: 'absolute',
							inset: 0,
							background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%)',
						}}
					/>
					<Box 
						sx={{
							width: 80,
							height: 80,
							borderRadius: '50%',
							backgroundColor: 'white',
							display: 'flex',
							alignItems: 'center',
							justifyContent: 'center',
							boxShadow: '0 10px 40px rgba(0,0,0,0.3)',
							position: 'relative',
							zIndex: 1,
							transition: 'all 0.3s ease',
							'&:hover': {
								transform: 'scale(1.1)',
								backgroundColor: '#3b82f6',
								'& .play-icon': {
									color: 'white'
								}
							},
						}}
					>
						<PlayArrowIcon sx={{ fontSize: 40, color: '#1e293b' }} className="play-icon" />
					</Box>
					<Typography 
						sx={{
							position: 'absolute',
							bottom: 24,
							left: '50%',
							transform: 'translateX(-50%)',
							color: 'white',
							fontWeight: 500,
							zIndex: 1,
						}}
					>
						Haz clic para ver el video
					</Typography>
				</Box>
			</Container>
		</section>
	);
};

export default VideoDemo;
