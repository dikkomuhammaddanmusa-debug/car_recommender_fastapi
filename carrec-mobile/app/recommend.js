import React, { useEffect, useState } from "react";
import { View, Text, ActivityIndicator, StyleSheet } from "react-native";
import { recommendCars } from "../src/api";

export default function Recommend() {
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    (async () => {
      try {
        const res = await recommendCars({ limit: 10 });
        setMsg(JSON.stringify(res.data).slice(0, 200));
      } catch (e) {
        setMsg(e?.response?.status ? `HTTP ${e.response.status}` : e?.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);
  if (loading) return <ActivityIndicator style={{ marginTop: 40 }} />;
  return (
    <View style={styles.wrap}>
      <Text style={styles.title}>Recommend</Text>
      <Text selectable>{msg}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { flex: 1, padding: 16 },
  title: { fontSize: 18, fontWeight: "700", marginBottom: 12 },
});
