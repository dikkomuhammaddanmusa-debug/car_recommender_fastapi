import React, { useState } from "react";
import { View, Text, Pressable, StyleSheet, ScrollView } from "react-native";
import { getStats } from "../api";

export default function StatsScreen() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  const go = async () => {
    setLoading(true);
    try {
      const { data } = await getStats();
      setStats(data);
    } catch (e) {
      console.warn(e?.response?.data || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.h1}>Stats</Text>
      <Pressable style={styles.btn} onPress={go} disabled={loading}>
        <Text style={styles.btnText}>{loading ? "Loading..." : "Load stats"}</Text>
      </Pressable>

      {stats && (
        <View style={{ marginTop: 12 }}>
          <Text>Total cars: {stats.total_cars}</Text>
          <Text style={{ marginTop: 8, fontWeight: "700" }}>Top brands:</Text>
          {Object.entries(stats.brand_counts_top25 || {}).map(([k, v]) => (
            <Text key={k}>{k}: {v}</Text>
          ))}
          <Text style={{ marginTop: 8, fontWeight: "700" }}>Fuel counts:</Text>
          {Object.entries(stats.fuel_counts || {}).map(([k, v]) => (
            <Text key={k}>{k}: {v}</Text>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 14 },
  h1: { fontSize: 20, fontWeight: "700", marginBottom: 10 },
  btn: { backgroundColor: "#111827", padding: 12, borderRadius: 8, marginTop: 6 },
  btnText: { color: "white", textAlign: "center", fontWeight: "600" },
});
