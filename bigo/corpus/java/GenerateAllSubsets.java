public class GenerateAllSubsets {
    public static void enumerate(int[] data, int index, StringBuilder current) {
        if (index == data.length) {
            System.out.println(current.toString());
            return;
        }
        enumerate(data, index + 1, current);
        int mark = current.length();
        current.append(data[index]).append(' ');
        enumerate(data, index + 1, current);
        current.setLength(mark);
    }
}
