import React from 'react';
import { Container, Typography, Box } from '@mui/material';

const partners = [
	{ name: 'Banco General', logo: '/images/partner-general.png' },
	{ name: 'Banco Nacional', logo: '/images/partner-nacional.png' },
	{ name: 'Caterpillar', logo: '/images/partner-stripe.png' },
	{ name: 'DGI', logo: '/images/partner-dgi.png' },
	{ name: 'Copa Airlines', logo: '/images/partner-copa.png' },
	{ name: 'SFEP', logo: '/images/partner-sfep.png' },
];

const Partners = () => {
	return (
		<section sx={{ py: { xs: 8, md: 10 }, backgroundColor: 'white' }}>
			<Container maxWidth="lg">
				<Box textAlign="center" mb={6}>
					<Typography 
						variant="h6" 
						sx={{ color: '#64748b', fontWeight: 500 }}
					>
						Integraciones y compatibilidad
					</Typography>
				</Box>

				<Box 
					sx={{
						display: 'flex',
						flexWrap: 'wrap',
						justifyContent: 'center',
						gap: { xs: 4, md: 8 },
						alignItems: 'center'
					}}
				>
					{partners.map((partner, index) => (
						<Box
							key={index}
							sx={{
								display: 'flex',
								alignItems: 'center',
								justifyContent: 'center',
								opacity: 0.6,
								transition: 'all 0.3s ease',
								'&:hover': {
									opacity: 1,
								},
								minWidth: 120,
							}}
						>
							<Box 
								sx={{
									height: 40,
									width: 120,
									backgroundColor: '#e2e8f0',
									borderRadius: 2,
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
								}}
							>
								<Typography sx={{ color: '#64748b', fontWeight: 600, fontSize: '0.75rem' }}>
									{partner.name}
								</Typography>
							</Box>
						</Box>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default Partners;
