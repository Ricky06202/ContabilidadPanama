import React, { useState } from 'react';
import { Container, Typography, Box, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const faqs = [
	{
		question: '¿Necesito ser contador para usar ContabilidadPanama?',
		answer: 'No, ContabilidadPanama está diseñado para ser intuitivo y fácil de usar. Tanto contadores como empresarios sin experiencia contable pueden usarlo. Además, nuestro equipo de soporte está disponible para ayudarte.',
	},
	{
		question: '¿Las facturas electrónicas son válidas ante la DGI?',
		answer: 'Sí, completamente. ContabilidadPanama está integrado con el sistema SFEP de la Dirección General de Ingresos (DGI) de Panamá. Todas las facturas que emitas serán válidas y cumplirán con los requisitos legales.',
	},
	{
		question: '¿Mis datos están seguros?',
		answer: 'Absolutamente. Utilizamos encriptación de nivel bancario (SSL/TLS) y nuestros servidores están ubicados en centros de datos seguros. Además, hacemos backups automáticos diarios de tu información.',
	},
	{
		question: '¿Puedo mudar mis datos desde otro sistema contable?',
		answer: 'Sí, nuestro equipo de soporte puede ayudarte a migrar tus datos desde sistemas como MYOB, QuickBooks, SAP, o cualquier otro. Contáctanos y te explicamos el proceso.',
	},
	{
		question: '¿Hay costos de instalación o mantenimiento?',
		answer: 'No, no hay costos ocultos. El precio que ves es el precio que pagas. No hay costos de instalación, mantenimiento ni actualizaciones. Todo está incluido en tu plan.',
	},
	{
		question: '¿Puedo probar gratis antes de decidir?',
		answer: 'Sí, el plan Básico es completamente gratis y puedes usarlo indefinidamente. Además, ofrezco 14 días de prueba gratis del plan Profesional para que puedas probar todas las funcionalidades.',
	},
];

const FAQ = () => {
	return (
		<section sx={{ py: { xs: 12, md: 16 }, backgroundColor: 'white' }}>
			<Container maxWidth="md">
				<Box textAlign="center" mb={8}>
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
						Preguntas Frecuentes
					</Typography>
					<Typography variant="h6" sx={{ color: '#64748b', mb: 6, maxWidth: '600px', mx: 'auto' }}>
						Todo lo que necesitas saber sobre ContabilidadPanama
					</Typography>
				</Box>

				<Box>
					{faqs.map((faq, index) => (
						<Accordion 
							key={index}
							sx={{
								backgroundColor: '#f8fafc',
								borderRadius: index === 0 ? '12px 12px 0 0' : index === faqs.length - 1 ? '0 0 12px 12px' : 0,
								border: '1px solid #e2e8f0',
								mb: 1,
								'&:before': {
									display: 'none',
								},
								boxShadow: 'none',
							}}
						>
							<AccordionSummary
								expandIcon={<ExpandMoreIcon sx={{ color: '#64748b' }} />}
								sx={{
									'& .MuiAccordionSummary-content': {
										mb: 1,
									},
								}}
							>
								<Typography variant="subtitle1" sx={{ fontWeight: 600, color: '#1e293b' }}>
									{faq.question}
								</Typography>
							</AccordionSummary>
							<AccordionDetails>
								<Typography variant="body2" sx={{ color: '#64748b', lineHeight: 1.8 }}>
									{faq.answer}
								</Typography>
							</AccordionDetails>
						</Accordion>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default FAQ;
