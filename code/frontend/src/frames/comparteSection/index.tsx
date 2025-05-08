import Button from '@myComponents/button';
import styles from './styles.module.scss';
import HappyBed from '@myImages/happyBed.png';

export default function ComparteSection() {
    return (
        <div className={styles.wrapper}>
            <div className={styles.left}>
                <p className={styles.title}>Compárte lujo, recibe recompensas.</p>
                <p className={styles.description}>
                    ¿Listo para ganar el 50 % de cada venta?
                    <br />
                    Únete a Familia Regina y desbloquea bonos exclusivos, puntos por compras y envíos gratis.
                    <br />
                    Comparte tu enlace único y recibe el 1 % de las ventas de tus referidos.
                    <br />
                    ¡Afíliate hoy y empieza a multiplicar tus ingresos!
                </p>
                <Button text='¡Afíliate hoy!' />
            </div>
            <div className={styles.right}>
                <img src={HappyBed} alt="Happy Bed" />
            </div>
        </div>
    )
}