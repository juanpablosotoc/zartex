import styles from './styles.module.scss';
import Bed from '@myImages/bed.png';
import Button from '@myComponents/button';

export default function BedCard() {
    return (
        <div className={styles.bedCard}>
            <img src={Bed} alt="Bed" loading="lazy" />
            <div className={styles.content}>
                <p className={styles.smallInvitation}>Descubre el lujo que tu hogar merece</p>
                <p className={styles.title}>Calidad que transforma tu lugar</p>
                <Button text="Comprar Cobertores" />
            </div>
        </div>
    );
}
