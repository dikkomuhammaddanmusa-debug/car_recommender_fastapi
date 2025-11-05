import React, { useState } from "react";
import { View, Text, Pressable, Image, StyleSheet, Alert } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { API_URL } from "../api";

export default function UploadScreen() {
  const [image, setImage] = useState(null);
  const [serverResp, setServerResp] = useState(null);

  const pickImage = async () => {
    const res = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7
    });
    if (!res.canceled && res.assets?.length) {
      setImage(res.assets[0]);
    }
  };

  const upload = async () => {
    if (!image) return Alert.alert("Pick an image first");
    const uri = image.uri;
    const filename = uri.split("/").pop() || "upload.jpg";
    const type = filename.endsWith(".png") ? "image/png" : "image/jpeg";

    const form = new FormData();
    form.append("file", { uri, name: filename, type });

    try {
      const response = await fetch(`${API_URL}/api/v1/upload/image`, {
        method: "POST",
        headers: { "Content-Type": "multipart/form-data" },
        body: form,
      });
      const data = await response.json();
      setServerResp(data);
    } catch (e) {
      Alert.alert("Upload failed", e.message);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Upload a car photo</Text>
      <Pressable style={styles.btn} onPress={pickImage}>
        <Text style={styles.btnText}>Choose from library</Text>
      </Pressable>
      {image && (
        <>
          <Image source={{ uri: image.uri }} style={styles.preview} />
          <Pressable style={styles.btn} onPress={upload}>
            <Text style={styles.btnText}>Upload to server</Text>
          </Pressable>
        </>
      )}
      {serverResp && (
        <View style={styles.card}>
          <Text style={styles.title}>Server Response</Text>
          <Text selectable>{JSON.stringify(serverResp, null, 2)}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 14 },
  h1: { fontSize: 20, fontWeight: "700", marginBottom: 10 },
  btn: { backgroundColor: "#111827", padding: 12, borderRadius: 8, marginTop: 6 },
  btnText: { color: "white", textAlign: "center", fontWeight: "600" },
  preview: { width: "100%", height: 220, marginTop: 10, borderRadius: 12 },
  card: { padding: 12, borderWidth: 1, borderColor: "#eee", borderRadius: 10, marginTop: 12 },
  title: { fontWeight: "700", marginBottom: 4 },
});
