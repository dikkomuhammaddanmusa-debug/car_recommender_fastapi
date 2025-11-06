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
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", padding: 16 },
  title: { fontSize: 22, fontWeight: "700", marginBottom: 24 },
  btn: { backgroundColor: "#222", paddingVertical: 12, paddingHorizontal: 18, borderRadius: 8, marginVertical: 8 },
  btnText: { color: "#fff", fontSize: 16, fontWeight: "600" },
});
