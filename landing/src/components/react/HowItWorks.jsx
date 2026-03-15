import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import HowItWorksIcon from '@mui/icons-material/HowToReg';
import SettingsIcon from '@mui/icons-material/Settings';
import ReceiptIcon from '@mui/icons-material/Receipt';

const HowItWorks = () => {
	const steps = [
		{
			number: '01',
			icon: <HowItWorksIcon sx={{ fontSize: 48, color: '#3b82f6' }} />,
			title: 'Regístrate Gratis',
			description: 'Crea tu cuenta en segundos. No requiere tarjeta de crédito.',
			image: '/images/step-register.png',
		},
		{
			number: '02',
			icon: <SettingsIcon sx={{ fontSize: 48, color: '#8b5cf6' }} />,
			title: 'Configura tu Empresa',
			description: 'Ingresa tu RUC, datos fiscales y configura tus preferencias.',
			image: '/images/step-configure.png',
		},
		{
			number: '03',
			icon: <ReceiptIcon sx={{ fontSize: 48, color: '#06b6d4' }} />,
			title: 'Comienza a Facturar',
			description: 'Emití facturas electrónicas DGI/SFEP inmediatamente.',
			image: '/images/step-invoice.png',
		},
	];

	return (
		<section sx={{ py: { xs: 12, md: 16 }, backgroundColor: '#f8fafc' }}>
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
						Comienza en minutos
					</Typography>
					<Typography variant="h6" sx={{ color: '#64748b', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Tres simples pasos para transformar tu contabilidad
					</Typography>
				</Box>

				<Box 
					sx={{
						display: 'grid',
						gridTemplateColumns: {
							xs: '1fr',
							md: 'repeat(3, 1fr)'
						},
						gap: 6,
						position: 'relative',
						'&::before': {
							content: '""',
							position: 'absolute',
							top: '80px',
							left: '20%',
							right: '20%',
							height: '2px',
							background: 'linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4)',
							display: { xs: 'none', md: 'block' }
						}
					}}
				>
					{steps.map((step, index) => (
						<Box 
							key={index}
							sx={{
								display: 'flex',
								flexDirection: 'column',
								alignItems: 'center',
								textAlign: 'center',
								position: 'relative',
								zIndex: 1
							}}
						>
							<Box 
								sx={{
									width: 120,
									height: 120,
									borderRadius: '50%',
									backgroundColor: 'white',
									border: '3px solid',
									borderColor: index === 0 ? '#3b82f6' : index === 1 ? '#8b5cf6' : '#06b6d4',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									mb: 3,
									boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
								}}
							>
								{step.icon}
							</Box>
							<Typography 
								sx={{
									fontSize: '4rem',
									fontWeight: 800,
									color: '#e2e8f0',
									position: 'absolute',
									top: 0,
									left: '50%',
									transform: 'translateX(-50%)',
									zIndex: -1
								}}
							>
								{step.number}
							</Typography>
							<Typography variant="h5" sx={{ fontWeight: 600, mb: 2, color: '#1e293b' }}>
								{step.title}
							</Typography>
							<Typography variant="body1" sx={{ color: '#64748b', maxWidth: '280px' }}>
								{step.description}
							</Typography>
						</Box>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default HowItWorks;
