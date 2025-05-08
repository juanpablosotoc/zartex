import { Link } from 'react-router-dom';
import styles from './styles.module.scss';
import Button from '@myComponents/button';

export default function Footer() {
    return (
        <footer className={styles.footer}>
            <div className={styles.linksWrapper}>
                <p className={styles.title}>Enlaces</p>
                <div className={styles.links}>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                </div>
            </div>
            <div className={styles.linksWrapper}>
                <p className={styles.title}>Enlaces</p>
                <div className={styles.links}>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                </div>
            </div>
            <div className={styles.linksWrapper}>
                <p className={styles.title}>Enlaces</p>
                <div className={styles.links}>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                    <Link to='/'>Inicio</Link>
                </div>
            </div>
            <div className={styles.becomeMember}>
                <p className={styles.title}>Become a member</p>
                <p className={styles.description}>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, quos.</p>
                <Button text='Become a member' />
            </div>
        </footer>
    )
}