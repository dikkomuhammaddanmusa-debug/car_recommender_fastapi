import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { useRouter } from "expo-router";
export default function Home() {
  const router = useRouter();
  const Btn = ({ label, to }) => (
    <Pressable style={styles.btn} onPress={() => router.push(to)}>
      <Text style={styles.btnText}>{label}</Text>
    </Pressable>
  );
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Car Recommender (Mobile)</Text>
      <Btn label="Search" to="/search" />
      <Btn label="Recommend" to="/recommend" />
      <Btn label="Upload Image" to="/upload" />
      <Btn label="Stats" to="/stats" />
    </View>
  );
}
const styles = StyleSheet.create({
  container: { flex: 1, padding: 18, gap: 12, justifyContent: "center" },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 10, textAlign: "center" },
  btn: { backgroundColor: "#111827", padding: 14, borderRadius: 10 },
  btnText: { color: "white", textAlign: "center", fontSize: 16, fontWeight: "600" },
});
