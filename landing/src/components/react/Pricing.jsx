import React from 'react';
import { Container, Typography, Box, Button, Paper } from '@mui/material';
import CheckIcon from '@mui/icons-material/Check';

const plans = [
	{
		name: 'Básico',
		price: 'Gratis',
		description: 'Perfecto para emprendedores',
		features: [
			'1 empresa',
			'Facturación básica',
			'Hasta 50 facturas/mes',
			'Reportes simples',
			'Soporte por email',
		],
		highlighted: false,
		buttonText: 'Comenzar gratis',
	},
	{
		name: 'Profesional',
		price: '$29',
		period: '/mes',
		description: 'Ideal para PYMES',
		features: [
			'1 empresa',
			'Facturación ilimitada',
			'DGI/SFEP completo',
			'Reportes avanzados',
			'Multi-usuario (3)',
			'Integración bancos',
			'Soporte prioritario',
		],
		highlighted: true,
		buttonText: 'Comenzar ahora',
	},
	{
		name: 'Enterprise',
		price: 'Custom',
		description: 'Para grandes empresas',
		features: [
			'Multi-empresa',
			'Facturación ilimitada',
			'API completa',
			'Usuarios ilimitados',
			'Integraciones personalizadas',
			'Gestor de cuenta dedicado',
			'Soporte 24/7',
			'Capacitación in-house',
		],
		highlighted: false,
		buttonText: 'Contactar ventas',
	},
];

const Pricing = () => {
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
						Planes para cada necesidad
					</Typography>
					<Typography variant="h6" sx={{ color: '#64748b', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Elige el plan que mejor se adapte a tu negocio. Sin sorpresas.
					</Typography>
				</Box>

				<Box 
					sx={{
						display: 'grid',
						gridTemplateColumns: {
							xs: '1fr',
							md: 'repeat(3, 1fr)'
						},
						gap: 4,
						alignItems: 'stretch'
					}}
				>
					{plans.map((plan, index) => (
						<Paper
							key={index}
							elevation={0}
							sx={{
								p: 4,
								height: '100%',
								borderRadius: 4,
								backgroundColor: plan.highlighted ? '#1e293b' : 'white',
								border: plan.highlighted ? 'none' : '1px solid #e2e8f0',
								position: 'relative',
								transition: 'all 0.3s ease',
								display: 'flex',
								flexDirection: 'column',
								'&:hover': {
									transform: 'translateY(-8px)',
									boxShadow: '0 20px 40px rgba(0,0,0,0.15)',
								},
							}}
						>
							{plan.highlighted && (
								<Box 
									sx={{
										position: 'absolute',
										top: -12,
										left: '50%',
										transform: 'translateX(-50%)',
										backgroundColor: '#3b82f6',
										color: 'white',
										px: 2,
										py: 0.5,
										borderRadius: '9999px',
										fontSize: '0.75rem',
										fontWeight: 600,
									}}
								>
									MÁS POPULAR
								</Box>
							)}
							<Typography 
								variant="h5" 
								sx={{ 
									fontWeight: 600, 
									mb: 1,
									color: plan.highlighted ? 'white' : '#1e293b'
								}}
							>
								{plan.name}
							</Typography>
							<Box sx={{ display: 'flex', alignItems: 'baseline', mb: 1 }}>
								<Typography 
									variant="h3" 
									sx={{ 
										fontWeight: 700, 
										color: plan.highlighted ? 'white' : '#1e293b'
									}}
								>
									{plan.price}
								</Typography>
								{plan.period && (
									<Typography 
										variant="body1" 
										sx={{ 
											color: plan.highlighted ? '#94a3b8' : '#64748b',
											ml: 1
										}}
									>
										{plan.period}
									</Typography>
								)}
							</Box>
							<Typography 
								variant="body2" 
								sx={{ 
									color: plan.highlighted ? '#94a3b8' : '#64748b',
									mb: 3
								}}
							>
								{plan.description}
							</Typography>
							<Box sx={{ flex: 1, mb: 3 }}>
								{plan.features.map((feature, i) => (
									<Box 
										key={i} 
										sx={{ 
											display: 'flex', 
											alignItems: 'center', 
											mb: 1.5 
										}}
									>
										<CheckIcon 
											sx={{ 
												fontSize: 20, 
												mr: 1.5,
												color: plan.highlighted ? '#3b82f6' : '#10b981'
											}} 
										/>
										<Typography 
											variant="body2" 
											sx={{ color: plan.highlighted ? '#e2e8f0' : '#475569' }}
										>
											{feature}
										</Typography>
									</Box>
								))}
							</Box>
							<Button
								variant={plan.highlighted ? 'contained' : 'outlined'}
								fullWidth
								href="https://app.contapanama.rsanjur.com"
								sx={{
									py: 1.5,
									fontWeight: 600,
									borderRadius: 2,
									textTransform: 'none',
									backgroundColor: plan.highlighted ? '#3b82f6' : 'transparent',
									borderColor: plan.highlighted ? '#3b82f6' : '#e2e8f0',
									color: plan.highlighted ? 'white' : '#1e293b',
									'&:hover': {
										backgroundColor: plan.highlighted ? '#2563eb' : '#f1f5f9',
									},
								}}
							>
								{plan.buttonText}
							</Button>
						</Paper>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default Pricing;
