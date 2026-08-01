public class EditDistance {
    public static int distance(String a, String b) {
        int n = a.length();
        int m = b.length();
        int[][] table = new int[n + 1][m + 1];
        for (int i = 0; i <= n; i++) table[i][0] = i;
        for (int j = 0; j <= m; j++) table[0][j] = j;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int cost = a.charAt(i - 1) == b.charAt(j - 1) ? 0 : 1;
                table[i][j] = Math.min(Math.min(table[i - 1][j] + 1,
                                                table[i][j - 1] + 1),
                                       table[i - 1][j - 1] + cost);
            }
        }
        return table[n][m];
    }
}
