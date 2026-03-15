import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import CloudDoneIcon from '@mui/icons-material/CloudDone';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';

const TrustBadges = () => {
	const badges = [
		{
			icon: <LockIcon sx={{ fontSize: 40, color: '#10b981' }} />,
			title: 'SSL Seguro',
			description: 'Encriptación de nivel bancario',
		},
		{
			icon: <VerifiedUserIcon sx={{ fontSize: 40, color: '#3b82f6' }} />,
			title: 'Cumple DGI',
			description: 'Facturación electrónica autorizada',
		},
		{
			icon: <CloudDoneIcon sx={{ fontSize: 40, color: '#8b5cf6' }} />,
			title: '99.9% Uptime',
			description: 'Disponibilidad garantizada',
		},
		{
			icon: <SupportAgentIcon sx={{ fontSize: 40, color: '#f59e0b' }} />,
			title: 'Soporte Local',
			description: 'Equipo en Panamá',
		},
	];

	return (
		<section sx={{ py: { xs: 8, md: 10 }, backgroundColor: '#f8fafc' }}>
			<Container maxWidth="lg">
				<Box 
					sx={{
						display: 'grid',
						gridTemplateColumns: {
							xs: 'repeat(2, 1fr)',
							md: 'repeat(4, 1fr)'
						},
						gap: 4
					}}
				>
					{badges.map((badge, index) => (
						<Box 
							key={index}
							sx={{
								display: 'flex',
								flexDirection: 'column',
								alignItems: 'center',
								textAlign: 'center',
								p: 3,
							}}
						>
							<Box 
								sx={{
									width: 64,
									height: 64,
									borderRadius: '50%',
									backgroundColor: 'white',
									display: 'flex',
									alignItems: 'center',
									justifyContent: 'center',
									mb: 2,
									boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
								}}
							>
								{badge.icon}
							</Box>
							<Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 0.5, color: '#1e293b' }}>
								{badge.title}
							</Typography>
							<Typography variant="body2" sx={{ color: '#64748b' }}>
								{badge.description}
							</Typography>
						</Box>
					))}
				</Box>
			</Container>
		</section>
	);
};

export default TrustBadges;
