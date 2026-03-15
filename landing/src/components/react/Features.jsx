import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import SpeedIcon from '@mui/icons-material/Speed';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import DevicesIcon from '@mui/icons-material/Devices';
import SecurityIcon from '@mui/icons-material/Security';
import CloudIcon from '@mui/icons-material/Cloud';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';

const Features = () => {
	const features = [
		{
			icon: <SpeedIcon sx={{ fontSize: 40, color: '#3b82f6' }} />,
			title: 'Ultra Rápido',
			description: 'Carga instantánea sin demoras. Interfaz moderna y fluida que mejora tu productividad diaria.',
			image: '/images/feature-speed.png',
			bgColor: '#dbeafe',
		},
		{
			icon: <AccountBalanceIcon sx={{ fontSize: 40, color: '#8b5cf6' }} />,
			title: 'DGI Integrado',
			description: 'Cumplimiento fiscal automático con la Dirección General de Ingresos de Panamá. Facturación electrónica SFEP.',
			image: '/images/feature-dgi.png',
			bgColor: '#ede9fe',
		},
		{
			icon: <CloudIcon sx={{ fontSize: 40, color: '#06b6d4' }} />,
			title: '100% en la Nube',
			description: 'Accede desde cualquier lugar. Tus datos siempre seguros y disponibles en tiempo real.',
			image: '/images/feature-cloud.png',
			bgColor: '#cffafe',
		},
		{
			icon: <SecurityIcon sx={{ fontSize: 40, color: '#10b981' }} />,
			title: 'Seguridad Bancaria',
			description: 'Tus datos protegidos con encriptación de nivel bancario. Cumplimiento con normativas de privacidad.',
			image: '/images/feature-security.png',
			bgColor: '#d1fae5',
		},
		{
			icon: <DevicesIcon sx={{ fontSize: 40, color: '#f59e0b' }} />,
			title: 'Multi-dispositivo',
			description: 'Web, móvil y escritorio. Tu contabilidad disponible en todos tus dispositivos.',
			image: '/images/feature-devices.png',
			bgColor: '#fef3c7',
		},
		{
			icon: <SupportAgentIcon sx={{ fontSize: 40, color: '#ef4444' }} />,
			title: 'Soporte Local',
			description: 'Equipo de soporte en Panamá. Estamos aquí para ayudarte cuando lo necesites.',
			image: '/images/feature-support.png',
			bgColor: '#fee2e2',
		},
	];

	return (
		<section sx={{ py: { xs: 12, md: 16 }, backgroundColor: 'white' }}>
			<Container maxWidth="lg">
				<Box textAlign="center" mb={12}>
					<Typography 
						variant="h3" 
						component="h2"
						sx={{ 
							fontWeight: 700, 
							fontSize: { xs: '2rem', md: '2.5rem' },
							mb: 3,
							color: '#0f172a'
						}}
					>
						Todo lo que necesitas para tu negocio
					</Typography>
					<Typography variant="h6" sx={{ color: '#64748b', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Una plataforma completa diseñada específicamente para las necesidades de empresas panameñas
					</Typography>
				</Box>

				<Grid container spacing={6} justifyContent="center">
					{features.map((feature, index) => (
						<Grid item xs={12} sm={6} md={4} key={index}>
							<Paper
								elevation={0}
								sx={{
									p: 3,
									height: '100%',
									borderRadius: 4,
									backgroundColor: '#f8fafc',
									border: '1px solid #e2e8f0',
									textAlign: 'center',
									transition: 'all 0.3s ease',
									'&:hover': {
										transform: 'translateY(-8px)',
										boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
									},
								}}
							>
								<Box 
									sx={{ 
										width: '100%',
										aspectRatio: '16/9',
										borderRadius: 2,
										overflow: 'hidden',
										mb: 3,
										backgroundColor: '#e2e8f0',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
									}}
								>
									<img 
										src={feature.image} 
										alt={feature.title}
										style={{
											width: '100%',
											height: '100%',
											objectFit: 'cover',
										}}
									/>
								</Box>
								<Box sx={{ 
									width: 56, 
									height: 56, 
									borderRadius: '16px', 
									display: 'flex', 
									alignItems: 'center', 
									justifyContent: 'center', 
									mx: 'auto',
									mb: 2, 
									backgroundColor: feature.bgColor 
								}}>
									{feature.icon}
								</Box>
								<Typography variant="h6" component="h3" sx={{ fontWeight: 600, mb: 1.5, color: '#1e293b' }}>
									{feature.title}
								</Typography>
								<Typography variant="body2" sx={{ color: '#64748b', lineHeight: 1.6 }}>
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
