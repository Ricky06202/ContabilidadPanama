import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import FormatQuoteIcon from '@mui/icons-material/FormatQuote';

const testimonials = [
	{
		name: 'Maria Elena Rodriguez',
		role: 'Contadora Pública',
		company: 'Rodriguez & Asociados',
		quote: 'ContabilidadPanama revolucionó mi forma de trabajar. Antes tardaba horas haciendo facturas manuales, ahora lo hago en minutos y DGI las valida automáticamente.',
		image: '/images/testimonial-1.png',
	},
	{
		name: 'Carlos Alberto Mendoza',
		role: 'Dueño de Restaurante',
		company: 'La Casa del Sabor',
		quote: 'Como pequeño empresario, necesitaba algo fácil de usar. ContabilidadPanama me ayuda a llevar mis finanzas sin ser contador. Totalmente recomendado.',
		image: '/images/testimonial-2.png',
	},
	{
		name: 'Laura Isabel Batista',
		role: 'Directora Financiera',
		company: 'TechCorp Panamá',
		quote: 'El manejo multi-empresa es perfecto para nuestros grupos. La integración con bancos y la automatización de payroll nos ahorró semanas de trabajo.',
		image: '/images/testimonial-3.png',
	},
];

const Testimonials = () => {
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
						Lo que dicen nuestros clientes
					</Typography>
					<Typography variant="h6" sx={{ color: '#64748b', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Miles de empresas panameñas ya confían en nosotros
					</Typography>
				</Box>

				<Box 
					sx={{
						display: 'grid',
						gridTemplateColumns: {
							xs: '1fr',
							md: 'repeat(3, 1fr)'
						},
						gap: 4
					}}
				>
					{testimonials.map((testimonial, index) => (
						<Box
							key={index}
							sx={{
								p: 4,
								borderRadius: 4,
								backgroundColor: '#f8fafc',
								border: '1px solid #e2e8f0',
								position: 'relative',
								transition: 'all 0.3s ease',
								'&:hover': {
									transform: 'translateY(-4px)',
									boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
								},
							}}
						>
							<FormatQuoteIcon 
								sx={{ 
									fontSize: 48, 
									color: '#3b82f6', 
									opacity: 0.3,
									position: 'absolute',
									top: 16,
									left: 16
								}} 
							/>
							<Typography 
								variant="body1" 
								sx={{ 
									color: '#475569', 
									mb: 3, 
									mt: 2,
									fontStyle: 'italic',
									lineHeight: 1.8
								}}
							>
								"{testimonial.quote}"
							</Typography>
							<Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
								<Box 
									sx={{
										width: 48,
										height: 48,
										borderRadius: '50%',
										backgroundColor: '#e2e8f0',
										display: 'flex',
										alignItems: 'center',
										justifyContent: 'center',
										fontWeight: 600,
										color: '#3b82f6'
									}}
								>
									{testimonial.name.split(' ').map(n => n[0]).join('')}
								</Box>
								<Box>
									<Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#1e293b' }}>
										{testimonial.name}
									</Typography>
									<Typography variant="body2" sx={{ color: '#64748b' }}>
										{testimonial.role}
									</Typography>
								</Box>
							</Box>
						</Box>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default Testimonials;
