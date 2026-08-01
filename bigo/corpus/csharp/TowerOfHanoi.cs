public class TowerOfHanoi
{
    public static int Move(int disks, char from, char to, char aux)
    {
        if (disks == 0) return 0;
        int moves = Move(disks - 1, from, aux, to);
        moves++;
        moves += Move(disks - 1, aux, to, from);
        return moves;
    }
}
