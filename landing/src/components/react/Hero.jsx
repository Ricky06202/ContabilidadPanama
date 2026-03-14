import React from 'react';
import { Button, Container, Typography, Box, Grid } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const Hero = () => {
	return (
		<section 
			style={{
				background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
				paddingTop: '100px',
				paddingBottom: '80px',
				minHeight: '100vh',
				display: 'flex',
				alignItems: 'center',
				boxSizing: 'border-box',
				position: 'relative',
				overflow: 'hidden',
			}}
		>
			<div style={{
				position: 'absolute',
				top: 0,
				left: 0,
				right: 0,
				bottom: 0,
				backgroundImage: 'radial-gradient(circle at 25% 25%, rgba(37, 99, 235, 0.15) 0%, transparent 50%), radial-gradient(circle at 75% 75%, rgba(124, 58, 237, 0.15) 0%, transparent 50%)',
				pointerEvents: 'none',
			}} />
			<Container maxWidth="xl">
				<Grid container spacing={6} alignItems="center">
					<Grid item xs={12} md={6}>
						<Box 
							display="flex" 
							flexDirection="column" 
							alignItems={{ xs: 'center', md: 'flex-start' }} 
							textAlign={{ xs: 'center', md: 'left' }}
							sx={{ gap: 3 }}
						>
							<Box 
								display="inline-flex" 
								alignItems="center" 
								gap={1}
								sx={{
									backgroundColor: 'rgba(37, 99, 235, 0.1)',
									border: '1px solid rgba(37, 99, 235, 0.3)',
									borderRadius: '9999px',
									px: 2,
									py: 0.5,
								}}
							>
								<span style={{ 
									width: 8, 
									height: 8, 
									borderRadius: '50%', 
									backgroundColor: '#22c55e',
									animation: 'pulse 2s infinite'
								}} />
								<Typography 
									variant="body2" 
									sx={{ 
										color: '#93c5fd',
										fontWeight: 500,
										fontSize: '0.875rem'
									}}
								>
									La contabilidad del futuro está aquí
								</Typography>
							</Box>
							<Typography 
								variant="h1" 
								component="h1"
								sx={{
									fontWeight: 800,
									fontSize: { xs: '2.5rem', md: '3.5rem', lg: '4rem' },
									color: 'white',
									lineHeight: 1.1,
									mb: 1,
								}}
							>
								Contabilidad{' '}
								<span style={{
									background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
									WebkitBackgroundClip: 'text',
									WebkitTextFillColor: 'transparent',
								}}>
									Inteligente
								</span>
								<br />para Panamá
							</Typography>
							<Typography 
								variant="h6" 
								component="p"
								sx={{
									color: '#94a3b8',
									maxWidth: '500px',
									fontSize: { xs: '1rem', md: '1.125rem' },
									mb: 1,
								}}
							>
								Plataforma moderna de contabilidad diseñada para contadores y empresarios panameños. 
								Cumple con DGI, facturar electrónicamente y maneja tu negocio desde cualquier lugar.
							</Typography>
							<Box 
								display="flex" 
								gap={2} 
								flexWrap="wrap" 
								justifyContent={{ xs: 'center', md: 'flex-start' }}
								mb={2}
							>
								{[
									'DGI / SFEP Integrado',
									'Facturación Electrónica',
									'Multi-empresa',
								].map((item, i) => (
									<Box key={i} display="flex" alignItems="center" gap={1}>
										<CheckCircleIcon sx={{ fontSize: 18, color: '#22c55e' }} />
										<Typography variant="body2" sx={{ color: '#e2e8f0' }}>
											{item}
										</Typography>
									</Box>
								))}
							</Box>
							<Box 
								display="flex" 
								gap={3} 
								flexWrap="wrap" 
								justifyContent={{ xs: 'center', md: 'flex-start' }}
							>
								<Button
									variant="contained"
									size="large"
									endIcon={<ArrowForwardIcon />}
									href="https://app.contapanama.rsanjur.com"
									sx={{
										background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
										px: 4,
										py: 1.5,
										fontSize: '1.1rem',
										fontWeight: 600,
										borderRadius: '12px',
										textTransform: 'none',
										'&:hover': {
											background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
										},
									}}
								>
									Comenzar ahora
								</Button>
							</Box>
						</Box>
					</Grid>
					<Grid item xs={12} md={6}>
						<Box 
							sx={{
								position: 'relative',
								borderRadius: '24px',
								overflow: 'hidden',
								boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
								border: '1px solid rgba(255, 255, 255, 0.1)',
								backgroundColor: 'rgba(255, 255, 255, 0.02)',
								aspectRatio: '16/10',
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
							}}
						>
							<img 
								src="/images/hero-dashboard.png" 
								alt="ContabilidadPanama Dashboard"
								style={{
									width: '100%',
									height: '100%',
									objectFit: 'cover',
								}}
							/>
						</Box>
					</Grid>
				</Grid>
			</Container>
			<style>{`
				@keyframes pulse {
					0%, 100% { opacity: 1; }
					50% { opacity: 0.5; }
				}
			`}</style>
		</section>
	);
};

export default Hero;
