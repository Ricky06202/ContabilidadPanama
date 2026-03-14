import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import SpeedIcon from '@mui/icons-material/Speed';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import DevicesIcon from '@mui/icons-material/Devices';

const Features = () => {
	const features = [
		{
			icon: <SpeedIcon sx={{ fontSize: 40, color: '#2563eb' }} />,
			title: 'Rapidez',
			description: 'Carga instantánea sin demoras. Olvídate de las interfaces lentas de los sistemas antiguos.',
			bgColor: '#dbeafe',
		},
		{
			icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#7c3aed' }} />,
			title: 'DGI Integrada',
			description: 'Cumplimiento fiscal automático con la Dirección General de Ingresos de Panamá.',
			bgColor: '#ede9fe',
		},
		{
			icon: <DevicesIcon sx={{ fontSize: 40, color: '#4f46e5' }} />,
			title: 'Multiplataforma',
			description: 'Usa la herramienta en web, móvil o escritorio. Tu contabilidad siempre contigo.',
			bgColor: '#e0e7ff',
		},
	];

	return (
		<section sx={{ pt: { xs: 12, md: 16 }, pb: { xs: 16, md: 24 }, backgroundColor: 'white' }}>
			<Container maxWidth="lg">
				<Box textAlign="center" mb={12}>
					<Typography 
						variant="h3" 
						component="h2"
						sx={{ 
							fontWeight: 700, 
							fontSize: { xs: '1.75rem', md: '2.25rem' },
							mb: 3 
						}}
					>
						¿Por qué elegirnos?
					</Typography>
					<Typography variant="h6" sx={{ color: 'text.secondary', mb: 6 }}>
						Una plataforma construida desde cero para las necesidades de Panamá
					</Typography>
				</Box>

				<Grid container spacing={8} justifyContent="center" sx={{ display: 'flex', flexDirection: 'row', flexWrap: { xs: 'wrap', md: 'nowrap' } }}>
					{features.map((feature, index) => (
						<Grid item sx={{ width: { md: '33%', xs: '100%' }, maxWidth: '350px' }} key={index}>
							<Paper
								elevation={0}
								sx={{
									p: 4,
									height: '100%',
									borderRadius: 3,
									backgroundColor: 'grey.50',
									border: '1px solid',
									borderColor: 'grey.200',
									textAlign: 'center',
									transition: 'all 0.3s ease',
									'&:hover': {
										transform: 'translateY(-4px)',
										boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
									},
								}}
							>
								<Box sx={{ 
									width: 64, 
									height: 64, 
									borderRadius: '50%', 
									display: 'flex', 
									alignItems: 'center', 
									justifyContent: 'center', 
									marginLeft: 'auto', 
									marginRight: 'auto', 
									mb: 3, 
									backgroundColor: feature.bgColor 
								}}>
									{feature.icon}
								</Box>
								<Typography variant="h5" component="h3" sx={{ fontWeight: 600, mb: 2 }}>
									{feature.title}
								</Typography>
								<Typography variant="body1" sx={{ color: 'text.secondary' }}>
									{feature.description}
								</Typography>
							</Paper>
						</Grid>
					))}
				</Grid>
			</Container>
		</section>
	);
};

export default Features;